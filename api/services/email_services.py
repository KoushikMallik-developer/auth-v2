from django.core.mail import EmailMessage


class EmailServices:
    def send_email(self, email_id):
        email = EmailMessage(
            "Hello",
            "Body goes here",
            "techomato.server@gmail.com",
            [email_id],
        )
        email.send()
