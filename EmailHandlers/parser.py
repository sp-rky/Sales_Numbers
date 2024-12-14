# this script checks an email inbox for an email labelled "budget MM/YY" with an excel spreadsheet attachment and parses the budget data from it to save to the database.
# sheer spaghetti BUT it works. and that's the important bit. 
# it's probably also pretty error prone - but that's okay. i still have like 3 more parts to this application to build so any bugs should iron themselves out by then... right?
import os
import sys  
import django
import pandas as pd
from calendar import monthrange
from datetime import datetime

# custom external libraries
import parserexceptions
from emailreader import Email

try:
    # django setup
    if os.environ.get("container") == "True":
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Sales_Numbers.settings')
        os.environ['PYTHONPATH'] = '/code'
        sys.path.append('/code')
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Sales_Numbers.settings')
        os.environ['PYTHONPATH'] = '/home/stephaniefletcher/Documents/Sales_Numbers'
        sys.path.append('/home/stephaniefletcher/Documents/Sales_Numbers')

    django.setup()
except Exception as e:
    print("Error: {e}")

# get the required django models
from SalesEntrySite.models import Store, DailyBudget

# convert the Store database into a nice, neat array of store numbers for easier data work
# bad for memory, but easy for this sleepy programmer, and it'll never be a particularly big list anyway
stores_list = Store.objects.order_by("store_num")
stores_list = [store.store_num for store in stores_list]

# get current working directory
working_directory = "/code"

# set up the email class
try:
    email = Email(os.environ.get("BudgetEmailAddress"), os.environ.get("BudgetEmailPassword"))
    email.select_inbox()
    latest_email = email.get_latest_email()
    subject_line = email.read_email_title(latest_email)
    if "budget" in subject_line:
        month = int(subject_line.split(" ")[1].split("/")[0])
        year = int("20" + subject_line.split(" ")[1].split("/")[1])
        email_attachments = email.get_email_attachments(latest_email)
        if len(email_attachments) == 1:
            email.save_attachment(latest_email, email_attachments[0], f"{working_directory}/BudgetFiles")
        budget_file = pd.ExcelFile(f"{working_directory}/BudgetFiles/{email_attachments[0]}")
        
    days_in_month = monthrange(year, month)[1]
except Exception as e:
    print(e)

# if there are any errors with the parsing, raise an exception and email the admins
#TODO: more robust error detection

number_of_new_entries = 0

try:
    # there should only be one sheet in the workbook
    if len(budget_file.sheet_names) != 1:
        raise parserexceptions.TooManySheetsError()

    # get the sheet that contains the budgets, and iterate through the rows
    budgets = pd.read_excel(budget_file, budget_file.sheet_names[0])
    for index, row in budgets.iterrows():
        # if the row we're looking at is in our stores database
        if row[1] in stores_list:
            # then parse the data from the sheet and save it to the database
            day_of_month = 1
            for budget in row[8:days_in_month+8]:
                budget_entry = DailyBudget(
                    store = Store.objects.get(store_num=row[1]),
                    date = datetime(year, month, day_of_month),
                    budget = budget
                )
                if not DailyBudget.objects.filter(store=Store.objects.get(store_num=row[1]), date=datetime(year, month, day_of_month)).exists():
                    budget_entry.save()
                    number_of_new_entries += 1
                day_of_month += 1
                

except Exception as e:
    #TODO: email the admins when something goes wrong
    print(e)
print(f"Parser has been run, updated {number_of_new_entries} rows.")



