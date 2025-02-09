import smtplib
from email_sender import Mail

class Email:
    def __init__(self, server, username, password):
        self.username = username
        self.server = smtplib.SMTP(server, 587)
        self.server.ehlo()
        self.server.starttls()
        self.server.login(self.username, password)

    def send(self, email: Mail):
        self.server.sendmail(self.username, email.to, email.mail)

if __name__ == '__main__':
    email = Mail('example@gmail.com', 'example@example.com', 'Hey how are you!', 'Hello there :)')

    gmail = Email('smtp.gmail.com', 'example@gmail.com', 'password123')
    gmail.send(email)
