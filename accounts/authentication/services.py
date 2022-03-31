from os import access
import jwt
from rest_framework_simplejwt.tokens import RefreshToken
from decouple import config


def generate_token():
    pass

def decode_token(token):
    
    try:
        verifying_key = get_verifying_key()
        data = jwt.decode(
                token,
                verifying_key,
                algorithms=["RS256"],
        )
    except (jwt.InvalidTokenError, jwt.ExpiredSignatureError, jwt.DecodeError) as exc:
        raise (str(exc))
    return data 

def get_verifying_key():
    key_path = config('JWT_PUBLIC_KEY_PATH')
    try:
        verifying_key = open(key_path).read()
        if verifying_key is not None:
            return verifying_key
    except (jwt.KeyError) as exc:
        raise (str(exc))

def authenticate():
    pass

def verify_token():
    pass

def jwt_payload_handler_user(user, token) : 
    access_token = token.access_token
    payload = {
        #'token_type':'access',
        'refresh':str(token),
        'access': str(token.access_token),
        'user_email':user.email,
    }

    return payload