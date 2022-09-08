from django.db import models

class Customer(models.Model):
    id = models.BigIntegerField(primary_key=True)
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50)
    isAdmin = models.BooleanField(default=False)

class Account(models.Model):
    number = models.IntegerField(primary_key=True)
    balance = models.DecimalField(max_digits=20, decimal_places=2)
    lastChangeDate = models.DateField()
    isActive = models.BooleanField(default=True)
    customer = models.ForeignKey(Customer, related_name='account', on_delete=models.CASCADE)

