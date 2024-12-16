from django.shortcuts import render
from django.template import loader

# Create your views here.
from django.http import HttpResponse
from .models import Store, Sale


def index(request):
    stores_list = Store.objects.order_by("store_num")
    context = {
        "stores_list": stores_list
    }

    return render(request, "SalesEntrySite/index.html", context)


def submit(request):
    store = int(request.POST.get('store'))
    # Check if the store exists in the database
    try:
        selected_store = Store.objects.get(store_num=store)
    except Store.DoesNotExist:
        return HttpResponse(f"Error: Store with number {store} does not exist.")
    
    # get the user input, throw an error if the data entered is incorrectly formatted or the user misses a entry field
    try:
        sales = int(request.POST.get('sales'))
        average_sale = float(request.POST.get('average_sale'))
        door_count = int(request.POST.get('door_count'))
    except ValueError:
        return HttpResponse("Invalid input. Please round to the nearest dollar. (Average Sale can be entered as a decimal)")
    except Exception as e:
        return HttpResponse(e)

    # save the data entered by the user to the database
    sale_entry = Sale(
        store = selected_store,
        sales = sales,
        average_sale = average_sale,
        door_count = door_count
    )
    sale_entry.save()

    # add the sales data to the context for the html template
    context = {
        "selected_store": selected_store,
        "sales": sales,
        "average_sale": average_sale,
        "door_count": door_count
    }

    return render(request, "SalesEntrySite/submit.html", context)
