import firebase_admin
from firebase_admin import credentials, auth
# Path to your service account JSON file
cred = credentials.Certificate("key.json")

# Initialize the Firebase Admin SDK
firebase_admin.initialize_app(cred)
class account_creation():
    def __init__(self):
        pass


    def create_firebase_account(self, name, password):
        user = auth.create_user(
            email=name,
            email_verified=False,
            password=password,
            disabled=False
    )



