from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from cards.models import Card
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient
import random, string, time
from typing import TypedDict

class Credentials(TypedDict):
    card_number: str
    ccv: str
    title: str = "title"


def authenticate_client(client, user):
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)


def generate_random_credentials() -> Credentials:
    credit_card_number = "".join(random.choices(string.digits, k=16))
    ccv = "".join(random.choices(string.digits, k=3))
    return {"card_number": credit_card_number, "ccv": ccv, "title": "string"}

class CardTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpassword"
        )
        self.client = APIClient()
        authenticate_client(self.client, self.user)


    def create_card(self, data: Credentials):
        """
        Helper method to create a new card object.
        """
        url = reverse("card-create-new-card")
        response = self.client.post(url, data, format="json")
        return response

    def test_create_card(self):
        """
        Ensure we can create a new card object.
        """
        
        data = generate_random_credentials()
   
        response = self.create_card(data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.assertEqual(Card.objects.get().isValid, False)

    def test_100_create_cards(self):
        start_time = time.time()

        for _ in range(0, 100):
            response = self.create_card(generate_random_credentials())
        end_time = time.time()
        time_taken = end_time - start_time

        maximum_time = 5
        self.assertLess(time_taken, maximum_time)
        
        print(f"Time taken to create 100 cards: {time_taken} seconds")