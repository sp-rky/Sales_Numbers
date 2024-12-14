import imaplib
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import decode_header
from email.message import EmailMessage
import os
from email.mime.base import MIMEBase
from email.encoders import encode_base64
import email
from datetime import datetime

class Email:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.mail = imaplib.IMAP4_SSL(os.environ.get("IMAPServer"), 993)
        self.login()
        self.select_inbox()

    def login(self):
        try:
            status, data = self.mail.login(self.username, self.password)
            if status != "OK":
                print(status)
                raise Exception("Could not log in to IMTP server.")
        except Exception as e:
            print(f"Error logging in: {e}")
            exit(1)

    def select_inbox(self):
        status, data = self.mail.select("inbox")
        if status != "OK":
            raise Exception("Could not select inbox.")

    def get_latest_email(self):
        status, messages = self.mail.search(None, 'ALL')
        if status != "OK":
            raise Exception("No messages found.")
        
        latest_email_id = messages[0].split()[-1]
        return latest_email_id

    def read_email_title(self, email_id):
        raw_email = self.fetch_email(email_id)
        msg = email.message_from_bytes(raw_email)
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or "utf-8")
        return subject

    def save_attachment(self, email_id, attachment_id, save_path):
        raw_email = self.fetch_email(email_id)
        msg = email.message_from_bytes(raw_email)
        
        for part in msg.walk():
            if part.get_content_maintype() == "multipart":
                continue
            if part.get('Content-Disposition') is None:
                continue
            
            filename = part.get_filename()
            if attachment_id in filename:
                with open(save_path + "/" + filename, "wb") as f:
                    f.write(part.get_payload(decode=True))
                # print(f"Attachment '{filename}' saved to {save_path + filename}")
    
    def fetch_email(self, email_id):
        status, data = self.mail.fetch(email_id, "(RFC822)")
        if status != "OK":
            raise Exception("Failed to fetch email.")
        return data[0][1]

    def get_email_attachments(self, email_id):
        raw_email = self.fetch_email(email_id)
        msg = email.message_from_bytes(raw_email)
        
        attachments = []
        for part in msg.walk():
            if part.get_content_maintype() == "multipart":
                continue
            if part.get('Content-Disposition') is None:
                continue
            
            filename = part.get_filename()
            if filename is not None:
                attachments.append(filename)
        
        return attachments

    def send_email(self, from_addr, to_addr, subject, body):
        msg = MIMEMultipart()
        msg['From'] = from_addr
        msg['To'] = to_addr
        msg['Subject'] = subject
        
        msg.attach(MIMEText(body, 'HTML'))
        
        try:
            with smtplib.SMTP_SSL(os.environ.get("SMTPServer"), 465) as server:
                server.login(self.username, self.password)
                text = msg.as_string()
                server.sendmail(from_addr, to_addr, text)
                print(f"Email sent successfully at {datetime.now().isoformat()}")
        except Exception as e:
            print(f"Error sending email: {e}")

    def get_sender_email(self, email_id):
        raw_email = self.fetch_email(email_id)
        msg = EmailMessage.from_bytes(raw_email)
        
        sender = msg.get('from', None)
        if sender is None:
            raise Exception("Could not find the sender's email address.")
        
        return sender