import string
import random
from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

TWILIO_ACCOUNT_SID=os.getenv('TWILIO_ACCOUNT_SID')
ACCOUNT_SID = os.environ.get('TWILIO_SID')
AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
client = Client(username=TWILIO_ACCOUNT_SID, password=AUTH_TOKEN)


class OtpHandler:
    phone_number = None

    def __init__(self, phone_number) -> None:
        self.phone_number = phone_number

    def send_otp(self):
        try:
            verify = client.verify.v2.services(ACCOUNT_SID).verifications.create(
                                                to=self.phone_number, channel='sms')
            print(verify.status)
            return True
        except Exception as e:
            print(e)
            return False
        
    
    def verify_otp(self, otp):
        try:    
            verification_check = client.verify.v2.services(ACCOUNT_SID).verification_checks.create(
                                                to=self.phone_number, code=otp)
            
            print(verification_check.status)
            
            if verification_check.status == 'approved':
                return True
    
            return False

        except Exception as e:
            print(e)
            return False
        

    def set_password(self):
        random_password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        return random_password