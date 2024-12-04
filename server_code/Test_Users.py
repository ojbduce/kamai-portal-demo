import anvil.files
from anvil.files import data_files
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
from datetime import datetime, timedelta
import random
from faker import Faker
import secrets

fake = Faker()

existing_users = [
    {
        "email": "john.doe@testdomain.com",
        "rememberMeId": "remember-me-id-123456",
        "firstName": "John",
        "lastName": "Doe",
        "verificationDate": (datetime.now() - timedelta(days=5)).isoformat()
    },
    {
        "email": "jane.smith@testdomain.com",
        "rememberMeId": "remember-me-id-789101",
        "firstName": "Jane",
        "lastName": "Smith",
        "verificationDate": (datetime.now() - timedelta(days=2)).isoformat()
    },
    {
        "email": "alice.johnson@testdomain.com",
        "rememberMeId": "remember-me-id-112233",
        "firstName": "Alice",
        "lastName": "Johnson",
        "verificationDate": (datetime.now() - timedelta(days=10)).isoformat()
    },
    {
        "email": "bob.brown@testdomain.com",
        "rememberMeId": "remember-me-id-445566",
        "firstName": "Bob",
        "lastName": "Brown",
        "verificationDate": (datetime.now() - timedelta(days=7)).isoformat()
    },
    {
        "email": "carol.wilson@testdomain.com",
        "rememberMeId": "remember-me-id-778899",
        "firstName": "Carol",
        "lastName": "Wilson",
        "verificationDate": (datetime.now() - timedelta(days=3)).isoformat()
    },
    {
        "email": "david.taylor@testdomain.com",
        "rememberMeId": "remember-me-id-101112",
        "firstName": "David",
        "lastName": "Taylor",
        "verificationDate": (datetime.now() - timedelta(days=8)).isoformat()
    },
    {
        "email": "eve.davis@testdomain.com",
        "rememberMeId": "remember-me-id-131415",
        "firstName": "Eve",
        "lastName": "Davis",
        "verificationDate": (datetime.now() - timedelta(days=1)).isoformat()
    },
    {
        "email": "frank.miller@testdomain.com",
        "rememberMeId": "remember-me-id-161718",
        "firstName": "Frank",
        "lastName": "Miller",
        "verificationDate": (datetime.now() - timedelta(days=4)).isoformat()
    },
    {
        "email": "grace.moore@testdomain.com",
        "rememberMeId": "remember-me-id-192021",
        "firstName": "Grace",
        "lastName": "Moore",
        "verificationDate": (datetime.now() - timedelta(days=6)).isoformat()
    },
    {
        "email": "henry.wright@testdomain.com",
        "rememberMeId": "remember-me-id-222324",
        "firstName": "Henry",
        "lastName": "Wright",
        "verificationDate": (datetime.now() - timedelta(days=9)).isoformat()
    },
]

def generate_new_user():
    return {
        "email": fake.email(),
        "rememberMeId": secrets.token_urlsafe(32),
        "verificationDate": datetime.now()
}

# def select_user(existing_weight=0):
#     if random.random() < existing_weight:
#         return random.choice(existing_users)
#     else:
#         new_user = generate_new_user()
#         existing_users.append(new_user)
#         return new_user

def select_user():
  new_user = generate_new_user()
  print(f"remember_me_id from generate_new_user: {new_user['rememberMeId']}")
  return new_user

