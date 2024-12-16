# Sales_Numbers
### A simple way of compiling and emailing sales data from multiple retail stores.

Sales_Numbers was built mostly as a "I wonder if I could build this" type project - the task carried out by this program is normally done semi manually using Google Forms at my company - and I figured having it fully automated could save a lot of headaches.

### So, what does it do?

Sales_Numbers carries out the following functions:

1. Runs a simple website that stores enter their sales data into, where they are stored in a database.
2. Checks an email inbox daily for an email containing a specific Excel spreadsheet, and parses it's budget data.
3. At a set time (configurable in the `crontab` file), the web app compiles these datapoints into a HTML table, which is then emailed to all the stores. 

The entire program is built to be run in a Docker container for portability. 

## Basic setup

1. Pull the latest Docker image: `docker pull ghcr.io/sp-rky/sales_numbers:[VERSION]`
2. Create a `docker-compose.yml` file: `touch docker-compose.yml`
3. Add this to your `docker-compose.yml` file with your text editor of choice (replacing the example values with your own email configuration and timezone):

```
services:
  web:
    image: ghcr.io/sp-rky/sales_numbers:[VERSION]
    ports:
      - "8000:8000"
    environment:
      - container=True
      - TZ=Australia/Perth
      - DomainName=example.com
      - IMAPServer=imap.mailexample.com
      - SMTPServer=smtp.mailexample.com
      - BudgetEmailAddress=budgets@example.com
      - BudgetEmailPassword=1234
      - SalesEmailAddress=sales@example.com
      - SalesEmailPassword=5678
      - ExtraEmailRecipients=example1@axample.com,example2@example.com
      - DjangoSecretKey=
```
4. Start the Docker container: `docker compose up -d`
5. Go to your browser and check that the container is running correctly by going to the following address: `localhost:8000/admin` and logging in with `admin` as the username and password.
6. **IMPORTANT**: Click on users, and create a new user, or update the password to the admin user!
7. Create your Store entries.
8. Either enter Budgets manually, or email them to your selected budget email address.
9. All done! Simply give the Docker container an internet address (Cloudflare Tunnels are an easy option for those just wanting to get this to work), and you're good to go!
