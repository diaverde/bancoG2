import datetime
import json
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.conf import settings
from rest_framework_simplejwt.backends import TokenBackend
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
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
        try:
            token = request.META.get('HTTP_AUTHORIZATION')[7:]
            tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
            valid_data = tokenBackend.decode(token, verify=False)
            #print(valid_data)
            if valid_data['user_id'] != id:
                raise Exception
        except:
            return HttpResponse("Credenciales inválidas. Acceso no autorizado", status=401)

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
            token = request.META.get('HTTP_AUTHORIZATION')[7:]
            tokenBackend = TokenBackend(algorithm=settings.SIMPLE_JWT['ALGORITHM'])
            valid_data = tokenBackend.decode(token, verify=False)
            #print(valid_data)
            if valid_data['user_id'] != id:
                raise Exception
        except:
            return HttpResponse("Credenciales inválidas. Acceso no autorizado", status=401)
        
        try:
            customer = Customer.objects.filter(id = id).first()
            if (not customer):
                return HttpResponseBadRequest("No existe cliente con esa cédula.")

            data = json.loads(request.body)
            if 'firstName' in data.keys():
                customer.firstName = data["firstName"]
            if 'lastName' in data.keys():
                customer.lastName = data["lastName"]
            if 'email' in data.keys():
                customer.email = data["email"]
            if 'password' in data.keys():
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

# Clases heredadas para mejorar el token a entregar
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(MyTokenObtainPairSerializer, self).validate(attrs)
        data.update({'id': self.user.id})
        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer