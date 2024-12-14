from django.db import models

# Create your models here.
class Store(models.Model):
        store_name = models.CharField(max_length=25)
        store_num = models.IntegerField(primary_key=True)
        store_email = models.CharField(max_length=50)


class Sale(models.Model):
        store = models.ForeignKey(Store, on_delete=models.CASCADE)
        sales = models.IntegerField()
        average_sale = models.FloatField()
        door_count = models.IntegerField()
        date_entered = models.DateField(auto_now_add=True)
        datetime_entered = models.TimeField(auto_now_add=True)

        def _str__(self):
                return f'Store: {self.store_num}\nSales: {self.sales}\nAverage Sale: {self.average_sale}\nDoor Count: {self.door_count}'
        
class DailyBudget(models.Model):
        store = models.ForeignKey(Store, on_delete=models.CASCADE)
        date = models.DateField()
        budget = models.IntegerField()