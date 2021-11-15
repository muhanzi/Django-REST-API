# works with both python 2 and 3
from __future__ import print_function

import africastalking
from django.conf import settings


class SMS:
    def __init__(self):
		# Set your app credentials
        self.api_key = settings.AFRICASTALKING["API_KEY"]
        self.username = settings.AFRICASTALKING["USERNAME"]

        # Initialize the SDK
        africastalking.initialize(self.username, self.api_key)

        # Get the SMS service
        self.sms = africastalking.SMS

    def send(self,recipients,message):
            # Set the numbers you want to send to in international format
            # recipients = ["+254713YYYZZZ", "+254733YYYZZZ"]

            # Set your message
            # message = "I'm a lumberjack and it's ok, I sleep all night and I work all day";

            # Set your shortCode or senderId
            # Your registered short code or alphanumeric, defaults to AFRICASTKNG.
            sender = "shortCode or senderId"
            try:
				# Thats it, hit send and we'll take care of the rest.
                # response = self.sms.send(message, recipients, sender)
                response = self.sms.send(message, recipients)
                # print("===== Africastalking response ======")
                # print("recipients: "+str(recipients)+" \nmessage: "+message)
                print (response)
                responseMessage = response["SMSMessageData"]["Message"]
                responseStatus = response["SMSMessageData"]["Recipients"][0]  # get results for recipient at index 0
                # 101 is the status code for when the message was sent
                if responseStatus["statusCode"] == 101: 
                    return True
                else:    
                    return False
            except Exception as e:
                print ('Encountered an error while sending: %s' % str(e))
                return False

if __name__ == '__main__':
    SMS().send(recipients=["+254713YYYZZZ", "+254733YYYZZZ"],message="test sms")                