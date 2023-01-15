import threading
from django.conf import settings
from django.core.mail import send_mail


class EmailThread(threading.Thread):

    def __init__(self,  message, recipient_list):

        self.subject = "User Credentials"
        self.message = message
        self.sender = settings.EMAIL_HOST_USER
        self.recipient_list = recipient_list
        threading.Thread.__init__(self)

    def run(self):

        send_mail(
            self.subject,
            self.message,
            self.sender,
            self.recipient_list
        )