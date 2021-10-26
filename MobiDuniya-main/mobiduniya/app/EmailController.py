import email
import smtplib
import ssl
import base64
import os
import pathlib

from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email import encoders

from pdfconvertor import InvoiceGenerator as ig





class MailAssistant():
    
    sender_email = "mobiduniya2021"
    sender_password = "Mobi@2021#Duniya"
    reciever_email = ""
    body = ""
    subject = ""
    
    def __addAttachments(self,pdf_file):
        
        path = pdf_file
        fileName = os.path.basename(path)
        File = MIMEApplication(open(path, 'rb').read())
        File.add_header('Content-Disposition', 'attachment', filename=fileName)
        return File

    def __emailSkeleton(self,pdf_file):
        message = MIMEMultipart()

        message['From'] = self.sender_email
        message['To'] = self.reciever_email
        message['Subject'] = self.subject
        
        message.attach(MIMEText(self.body, "plain"))
        message.attach(self.__addAttachments(pdf_file))
        
        return message.as_string()

    def __sendMail(self,message):
        server = smtplib.SMTP("smtp.gmail.com",587)
        server.ehlo()
        server.starttls()
        
        if self.reciever_email != "" and message != "":
            server.login(self.sender_email, self.sender_password)
            server.sendmail(self.sender_email, self.reciever_email, message)
            server.close()
            return True
        else:
        	server.close()
        	return False

    def sendInvoice(self):
        ig.set_data(ig,userID=101,
                    username="Armaan Agrawal",
                    mob_num=9876543210,
                    house_num="101",
                    landmark="ABC School",
                    city="Indore",
                    state="Madhya Pradesh",
                    pincode=452010,
                    products=["Vivo V20 Pro","Xiaomi MI Note 10 Pro"],
                    billing_amt=45570)
        invoice = ig.generate_invoice(ig)
        #self.reciever_email = userID.email
        self.reciever_email = "armngrwl1299@gmail.com"
        self.subject = "Invoice of Purchase"
        self.body = "Thank you for making a purchase from MobiDuniiya"
        message = self.__emailSkeleton(invoice)
        return self.__sendMail(message)

ma = MailAssistant()
ma.sendInvoice()