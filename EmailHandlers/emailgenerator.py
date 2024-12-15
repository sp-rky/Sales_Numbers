import os
import sys
import django
from datetime import datetime, date, time
from emailreader import Email
from numpy import average

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
    print(f"Error: {e}")


from SalesEntrySite.models import Sale, Store, DailyBudget

table = []
area_sales = 0
area_averages = []
area_door_count = 0
area_number_of_sales = 0
area_budget = 0

current_date = date.today()

# this part of the script creates an list representation of the final email table 
stores_list = Store.objects.order_by("store_num")
for store in stores_list:
    # get the latest sale entry from a store that was made today
    # lazy! works though :D (exception is run if the store has not made an entry today)
    try:
        latest_sale_entry = Sale.objects.order_by("-datetime_entered").filter(store=store, date_entered=current_date)[0]

        sales = f'${latest_sale_entry.sales}'
        average_sale = f'${round(latest_sale_entry.average_sale)}'
        door_count = latest_sale_entry.door_count
        number_of_sales = round(latest_sale_entry.sales / latest_sale_entry.average_sale)
        raw_conversion_rate = number_of_sales / door_count

        # let the HTML converter know to highlight this entry red (note the "r!")
        if raw_conversion_rate < 0.6:
            conversion_rate = f'r!{round(raw_conversion_rate * 100)}%'
        else:
            conversion_rate = f'{round(raw_conversion_rate * 100)}%'

        budget_entry = DailyBudget.objects.get(store=store, date=current_date)
        budget = f'${budget_entry.budget}'
        percentage_of_budget = f'{round(latest_sale_entry.sales / budget_entry.budget * 100)}%'
        
        # keep a running total of some entries, others are stored in an array to be averaged later
        area_sales += latest_sale_entry.sales
        area_averages.append(latest_sale_entry.average_sale)
        area_door_count += latest_sale_entry.door_count
        area_number_of_sales += number_of_sales
        area_budget += budget_entry.budget
    except:
        sales = ""
        average_sale = ""
        door_count = ""
        number_of_sales = ""
        conversion_rate = ""
        budget_entry = DailyBudget.objects.get(store=store, date=current_date)
        budget = f'${budget_entry.budget}'
        percentage_of_budget = ""
        area_budget += budget_entry.budget

    # compile the final row data into a list, and append it to the table
    table_row = [store.store_name, sales, average_sale, door_count, number_of_sales, conversion_rate, budget, percentage_of_budget]
    table.append(table_row)

# add the area totals/averages to the table
# this section errors out if nobody submits their numbers - but that's fine because if nobody submits their numbers then there's no reason to send the email
# (it's not a bug, it's a feature)
try:
    area_percentage_of_budget = f'{round((area_sales / area_budget) * 100)}%'
    area_sales = f'${area_sales}'
    area_average = f'${round(average(area_averages))}'
    area_conversion_rate = f'{round((area_number_of_sales / area_door_count) * 100)}%'

    table.append(["a!Area", area_sales, area_average, area_door_count, area_number_of_sales, area_conversion_rate, f'${area_budget}', area_percentage_of_budget])
except Exception as e:
    print(f"Error: {e}")

# build the HTML table
with open("emailhtmlheader.html") as f:
    email_content = f.read()
email_content += '<table border="1">\n'
email_content += '<tr><th>Store</th><th>Sales</th><th>Average Sale</th><th>Door Count</th><th>Number of Sales</th><th>Conversion Rate</th><th>Budget</th><th>Percentage to Budget</th>'
for row in table:
    email_content += '<tr>\n'
    for entry in row:
        if "r!" in str(entry):
            # highlight the cell red
            email_content += f'<td id="HIGHLIGHTED">{str(entry)[2:]}</td>\n'
        elif "a!" in str(entry):
            # and add an empty row before the entry
            email_content += '<td colspan="8" id="BOLD">Area Sales:</td>\n</tr>\n<tr>'
            email_content += f'<td>{str(entry[2:])}</td>'
        else:
            email_content += f'<td>{entry}</td>\n'
    email_content += '  </tr>\n'

email_content += '</table>'

email_content += f'\n<p>Generated on {datetime.now().strftime("%d/%m/%Y")} at {datetime.now().strftime("%H:%M:%S")}.</p>'

email = Email(os.environ.get("SalesEmailAddress"), os.environ.get("SalesEmailPassword"))
email_addresses = [store.store_email for store in Store.objects.order_by("store_num")] + os.environ.get("ExtraEmailRecipients").split(",")
email.send_email("salesnumbers@jaycarsalesentry.com", email_addresses, f"1PM Numbers {current_date.isoformat()}", email_content)

