import environ
import json
from rest_framework import authentication
from firebase_admin import credentials, initialize_app, auth
from .exceptions import FirebaseError, InvalidAuthToken, NoAuthToken
from .models import User


env = environ.Env()
environ.Env.read_env('tutorbook_django/.env')

config = {
  'type': 'service_account',
  'project_id': env('FIREBASE_PROJECT_ID'),
  'private_key_id': env('FIREBASE_PRIVATE_KEY_ID'),
  'private_key': env('FIREBASE_PRIVATE_KEY').replace('\\n', '\n'),
  'client_email': env('FIREBASE_CLIENT_EMAIL'),
  'client_id': env('FIREBASE_CLIENT_ID'),
  'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
  'token_uri': 'https://oauth2.googleapis.com/token',
  'auth_provider_x509_cert_url': 'https://www.googleapis.com/oauth2/v1/certs',
  'client_x509_cert_url': env('FIREBASE_CLIENT_CERT_URL')
}

cred = credentials.Certificate(config)

app = initialize_app(cred)

class FirebaseAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        # Ensure that an authentication token is present
        auth_header = request.META.get('HTTP_AUTHORIZATION')
        print(auth_header)
        if not auth_header:
            raise NoAuthToken()
        # Verify the token using the verify_id_token function
        id_token = auth_header.split(' ').pop()
        decoded_token = None
        try:
            decoded_token = auth.verify_id_token(id_token)
        except Exception:
            raise InvalidAuthToken()
        print(decoded_token)
        if not id_token or not decoded_token:
            return None
        # Get user
        try:
            email = decoded_token['email']
        except Exception:
            raise FirebaseError()
        # Return user
        user = User.objects.get(email=email)
        print(user)
        return (user, None)
