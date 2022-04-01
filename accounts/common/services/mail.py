from django.core.mail import EmailMessage
from smtplib import SMTPException

class MyMail: 
    def __init__(self, subject, body, email_address):
        self.email = EmailMessage(
                        subject, 
                        body, 
                        email_address
                    )
    
    def send(self):
        try:
            self.email.send()
        except SMTPException as e:          # It will catch other errors related to SMTP.
            print('There was an error sending an email.'+ e)
        except:                             # It will catch All other possible errors.
            print("Mail Sending Failed!")