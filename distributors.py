
import smtplib
import email

class DistributeToDistributor(object):
    def __init__(self, recipients, distributor):
        self.recipients = recipients
        self.distributor = distributor

    def distribute(self, mail):
        mail.ml_send_to = self.recipients
        self.distributor.distribute(mail)

class SmtpDistributor(object):
    def __init__(self, host='localhost', user=None, password='', ssl=False, tls=False, sender=None):
        if ssl:
            self.smtp = smtplib.SMTP_SSL(host)
        else:
            self.smtp = smtplib.SMTP(host)
        if tls:
            self.smtp.ehlo()
            self.smtp.starttls()
            self.smtp.ehlo()
        if user:
            self.smtp.login(user, password)
        self.sender = sender
    
    def distribute(self, mail):
        if self.sender:
            sender = self.sender
        else:
            sender = mail.ml_sender
        for recipient in mail.ml_send_to:
            self.smtp.sendmail(sender, recipient, mail.as_string())
    
    def __del__(self):
        self.smtp.quit()

class MultipleDistributor(object):
    def __init__(self, *args):
        self.distributors = args

    def distribute(self, mail):
        for distributor in self.distributors:
            distributor.distribute(mail)

