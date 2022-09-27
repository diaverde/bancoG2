from http import client
import json
from os import access
from urllib import response
import jwt
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

# Create your tests here.
class TestAPI(TestCase):
    def test_register(self):
        client = APIClient()
        testUser = {
            "id": 123456,
            "firstName": "test",
            "lastName": "user",
            "email": "test@user.com",
            "password": "12345"
        }
        response = client.post('/newCustomer', testUser, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, "Nuevo cliente agregado")

    def test_login(self):
        client = APIClient()
        testUser = {
            "id": 123456,
            "firstName": "test",
            "lastName": "user",
            "email": "test@user.com",
            "password": "12345"
        }
        response = client.post('/newCustomer', testUser, format='json')
        
        testLoginData = {
            "email": "test@user.com",
            "password": "12345"
        }
        response = client.post('/login', testLoginData, format='json')
        tokenData = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in tokenData.keys())
        self.assertTrue('refresh' in tokenData.keys())
        self.assertTrue('id' in tokenData.keys())

    def test_getCustomer(self):
        client = APIClient()
        testUser = {
            "id": 123456,
            "firstName": "test",
            "lastName": "user",
            "email": "test@user.com",
            "password": "12345"
        }
        response = client.post('/newCustomer', testUser, format='json')
        
        testLoginData = {
            "email": "test@user.com",
            "password": "12345"
        }
        response = client.post('/login', testLoginData, format='json')
        
        tokenData = json.loads(response.content)
        accessToken = tokenData['access']
        id = tokenData['id']
        url = '/getOneCustomer/' + str(id)
        auth_headers = {'HTTP_AUTHORIZATION': 'Bearer ' + accessToken}
        
        response = client.get(url, **auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        userData = json.loads(response.content)
        self.assertEqual(userData['id'], 123456)
        self.assertEqual(userData['firstName'], 'test')
        self.assertEqual(userData['email'], 'test@user.com')