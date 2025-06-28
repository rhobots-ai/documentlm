import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
import requests
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from jwt.utils import base64url_decode

from config import settings

# Better Auth configuration
DEEPCITE_AUTH_EP = settings.DEEPCITE_AUTH_EP
DEEPCITE_AUTH_ISSUER = 'http://localhost:10000'
DEEPCITE_AUTH_JWKS_URL = f"{DEEPCITE_AUTH_EP}/api/auth/jwks"
DEEPCITE_AUTH_SIGNUP_URL = f"{DEEPCITE_AUTH_EP}/api/auth/sign-up/email"
DEEPCITE_AUTH_SIGNIN_URL = f"{DEEPCITE_AUTH_EP}/api/auth/sign-in/email"
DEEPCITE_AUTH_AUDIENCE = 'http://localhost:10000'

def get_jwks():
    response = requests.get(DEEPCITE_AUTH_JWKS_URL)
    response.raise_for_status()
    return response.json()

def get_signing_key(jwks, token):
    unverified_header = jwt.get_unverified_header(token)
    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            if key["kty"] == "OKP" and key["crv"] == "Ed25519":  # EdDSA key
                x = base64url_decode(key["x"])
                return Ed25519PublicKey.from_public_bytes(x)
            else:
                raise InvalidTokenError(f"Unsupported key type: {key['kty']}/{key.get('crv')}")
    raise InvalidTokenError("No matching key found in JWKS")


def verify_better_auth_token(token):
    try:
        # 1. Get JWKS
        jwks = get_jwks()

        # 2. Get the appropriate signing key
        signing_key = get_signing_key(jwks, token)

        # 3. Verify the token
        payload = jwt.decode(
            token,
            key=signing_key,
            algorithms=["EdDSA"],  # Better Auth uses RS256
            audience=DEEPCITE_AUTH_AUDIENCE,
            issuer=DEEPCITE_AUTH_ISSUER,
            options={
                "require": ["exp", "iat", "aud", "iss"],
                "verify_signature": True,
                "verify_aud": True,
                "verify_iss": True,
                "verify_exp": True,
            }
        )

        return payload

    except ExpiredSignatureError:
        return {"error": "Token expired"}
    except InvalidTokenError as e:
        return {"error": f"Invalid token: {str(e)}"}
    except Exception as e:
        return {"error": f"Verification failed: {str(e)}"}