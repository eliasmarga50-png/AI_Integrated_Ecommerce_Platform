

from __future__ import annotations
import hashlib
import hmac
import secrets
import uuid
from datetime import timedelta
from django.utils import timezone

def generate_transaction_reference(prefix:str="PAY")->str:
	token=secrets.token_hex(8).upper()
	
	return f"{prefix} - {token}"

def generate_idempotency_key()->str:
	
	return str(uuid.uuid4())
	
def generate_nonce(length:int=32)->str:
	return secrets.token_urlsafe(length)
	
def calculate_hmac_signature(
    payload: bytes,
    secret: str,
    algorithm=hashlib.sha-256,
)->str:
	
	return hmac.new(
	  key=secret.encode("utf-8"),
	  msg=payload,
	  digestmod=algorithm,
	).hexdigest()
	
	
def verify_hmac_signature(
    payload : bytes,
    secret : str,
    recevied_signature : str,
)->bool:
	expected_signature=calculate_hmac_generation(
	   payload=payload,
	   secret=secret,
	)
	
	return hmac.compare_digest(
	    expected_signature,
	    received_signature,
	)
	
def calculate_payload_hash()->str:
	
def is_timestamp_valid()->bool: