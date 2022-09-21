import datetime
import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.db.models import Q

from .models import Customer, Account

def home(request):
    return HttpResponse("Bienvenida a su banco.")

def newCustomer(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            customer = Customer.objects.filter(id = data['id']).first()
            if (customer):
                return HttpResponseBadRequest("Ya existe cliente con esa cédula.")

            customer = Customer(
                id = data["id"],
                firstName = data["firstName"],
                lastName = data["lastName"],
                email = data["email"],
                password = data["password"],
            )
            customer.save()
            return HttpResponse("Nuevo cliente agregado")
        except:
            return HttpResponseBadRequest("Error en los datos enviados")
    else:
        return HttpResponseNotAllowed(['POST'], "Método inválido")

def getAllCustomers(request):
    if request.method == 'GET':
        customers = Customer.objects.all()
        if (not customers):
            return HttpResponseBadRequest("No hay clientes en la base de datos.")

        allCustData = []
        for x in customers:
            data = {"id": x.id, "firstName": x.firstName, "lastName": x.lastName, "email": x.email}
            allCustData.append(data)
        dataJson = json.dumps(allCustData)
        #print(dataJson)
        resp = HttpResponse()
        resp.headers['Content-Type'] = "text/json"
        resp.content = dataJson
        return resp
    else:
        return HttpResponseNotAllowed(['GET'], "Método inválido")

def getOneCustomer(request, id):
    if request.method == 'GET':
        customer = Customer.objects.filter(id = id).first()
        if (not customer):
            return HttpResponseBadRequest("No existe cliente con esa cédula.")

        accounts = Account.objects.filter(customer = id)
        accountsData = []
        for acc in accounts:
            data = {"number": acc.number, "balance": float(acc.balance)}
            accountsData.append(data)

        data = {
            "id": customer.id,
            "firstName": customer.firstName,
            "lastName": customer.lastName,
            "email": customer.email,
            "accounts": accountsData
        }
        dataJson = json.dumps(data)
        resp = HttpResponse()
        resp.headers['Content-Type'] = "text/json"
        resp.content = dataJson
        return resp
    else:
        return HttpResponseNotAllowed(['GET'], "Método inválido")

def updateCustomer(request, id):
    if request.method == 'PUT':
        try:
            customer = Customer.objects.filter(id = id).first()
            if (not customer):
                return HttpResponseBadRequest("No existe cliente con esa cédula.")

            data = json.loads(request.body)
            customer.firstName = data["firstName"]
            customer.lastName = data["lastName"]
            customer.email = data["email"]
            customer.password = data["password"]
            customer.save()
            return HttpResponse("Cliente actualizado")
        except:
            return HttpResponseBadRequest("Error en los datos enviados")
    else:
        return HttpResponseNotAllowed(['PUT'], "Método inválido")

def deleteCustomer(request, id):
    if request.method == 'DELETE':
        try:
            customer = Customer.objects.filter(id = id).first()
            if (not customer):
                return HttpResponseBadRequest("No existe cliente con esa cédula.")

            customer.delete()
            return HttpResponse("Cliente eliminado")
        except:
            return HttpResponseBadRequest("Error en los datos enviados")
    else:
        return HttpResponseNotAllowed(['DELETE'], "Método inválido")

#-----------------
# Account
#-----------------

def newAccount(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            cust = Customer.objects.filter(id = data["userId"]).first()
            if (not cust):
                return HttpResponseBadRequest("No existe cliente con esa cédula.")
            
            account = Account(
                number = data["number"],
                lastChangeDate = datetime.datetime.now(),
                customer = cust
            )
            account.save()
            return HttpResponse("Nueva cuenta agregada")
        except:
            return HttpResponseBadRequest("Error en los datos enviados")
    else:
        return HttpResponseNotAllowed(['POST'], "Método inválido")

def updateAccount(request, id):
    if request.method == 'PUT':
        try:
            account = Account.objects.filter(number = id).first()
            if (not account):
                return HttpResponseBadRequest("No existe esa cuenta.")

            data = json.loads(request.body)
            account.balance = data["balance"]
            account.isActive = data["isActive"]
            account.save()
            return HttpResponse("Cuenta actualizada")
        except:
            return HttpResponseBadRequest("Error en los datos enviados")
    else:
        return HttpResponseNotAllowed(['PUT'], "Método inválido")

def deleteAccount(request, id):
    if request.method == 'DELETE':
        try:
            account = Account.objects.filter(number = id).first()
            if (not account):
                return HttpResponseBadRequest("No existe esa cuenta.")

            account.delete()
            return HttpResponse("Cuenta eliminada")
        except:
            return HttpResponseBadRequest("Error en los datos enviados")
    else:
        return HttpResponseNotAllowed(['DELETE'], "Método inválido")

#-----------------
# Login
#-----------------

def login(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data['email']
            password = data['password']

            customer = Customer.objects.filter(email = email, password = password).first()
            if (not customer):
                return HttpResponse("Credenciales inválidas.", status=401)

            custData = {"id": customer.id}
            resp = HttpResponse()
            resp.headers['Content-Type'] = "text/json"
            resp.content = json.dumps(custData)
            return resp
        except:
            return HttpResponseBadRequest("Error en los datos enviados")
    else:
        return HttpResponseNotAllowed(['POST'], "Método inválido")