from pickle import NONE
from fpdf import FPDF
import datetime

class InvoiceGenerator():
    '''
    CUSTOMER_ID = str(101) #from DB (current user's ID)
    CUSTOMER = "Armaan Agrawal, 9876543210" #Current user (<username>+", "+<contact_no>)
    ADDRESS = "112, Ring Road, Indore, Madhya Pradesh, 452010" #from DB (<house no>+" ("+<landmark>+"), "+<city>+", ("+<state>+"), "+<pincode>)
    DATE_OF_PURCHASE = str(datetime.date.today())
    INVOICE_NUMBER = ''.join(str(datetime.date.today()).split("-")) + str(datetime.datetime.now().strftime("%H%M%S")) + CUSTOMER_ID
    PRODUCT_NAME = "Vivo V20 Pro" #<brand name> + " " + <product name>
    BILLING_AMT = "Rs. "+str(25000) #Final Billing Amount from cart section
    '''
    CUSTOMER_ID = None
    CUSTOMER = None
    ADDRESS = None
    DATE_OF_PURCHASE = None
    INVOICE_NUMBER = None
    PRODUCT_NAME = None
    BILLING_AMT = None

    def set_data(self,userID,username,mob_num,house_num,landmark,city,state,pincode,products,billing_amt):
        self.CUSTOMER_ID = str(userID)
        self.CUSTOMER = username + str(mob_num)
        self.ADDRESS = house_num + " (" + landmark + "), " + city + " (" + state + "), " + str(pincode)
        self.DATE_OF_PURCHASE = str(datetime.date.today())
        self.INVOICE_NUMBER = ''.join(str(datetime.date.today()).split("-")) + str(datetime.datetime.now().strftime("%H%M%S")) + self.CUSTOMER_ID
        self.PRODUCT_NAME = ', '.join(products)
        self.BILLING_AMT = "Rs. " + str(billing_amt)

    def generate_invoice(self):
        pdf = FPDF()
        pdf.add_page()

        pdf.set_font("Arial", 'BI', size = 40)
        pdf.cell(200, 10, txt = "MobiDuniya", ln = 1, align = 'C')

        pdf.cell(200, 30, txt = " ", ln = 2, align = 'C')

        pdf.set_font("Arial", 'BI', size = 20)
        pdf.cell(200, 10, txt = "Billed To : ", ln = 3, align = 'L')
        pdf.set_font("Arial", size = 15)
        pdf.cell(50, 8, txt = self.CUSTOMER, ln = 4, align = 'L')
        pdf.cell(50, 8, txt = self.ADDRESS, ln = 5, align = 'L')

        pdf.cell(200, 10, txt = " ", ln = 6, align = 'C')

        pdf.set_font("Arial", 'BI', size = 20)
        pdf.cell(200, 10, txt = "Date of Purchase : ", ln = 7, align = 'L')
        pdf.set_font("Arial", size = 15)
        pdf.cell(50, 8, txt = self.DATE_OF_PURCHASE, ln = 8, align = 'L')

        pdf.cell(200, 10, txt = " ", ln = 9, align = 'C')

        pdf.set_font("Arial", 'BI', size = 20)
        pdf.cell(200, 10, txt = "Product : ", ln = 10, align = 'L')
        pdf.set_font("Arial", size = 15)
        pdf.cell(50, 8, txt = self.PRODUCT_NAME, ln = 11, align = 'L')

        pdf.cell(200, 10, txt = " ", ln = 12, align = 'C')

        pdf.set_font("Arial", 'BI', size = 20)
        pdf.cell(200, 10, txt = "Billing Amount : ", ln = 13, align = 'L')
        pdf.set_font("Arial", size = 15)
        pdf.cell(50, 8, txt = self.BILLING_AMT, ln = 14, align = 'L')

        pdf.cell(200, 10, txt = " ", ln = 15, align = 'C')

        pdf.set_font("Arial", 'BI', size = 20)
        pdf.cell(200, 10, txt = "Invoice Number : ", ln = 16, align = 'L')
        pdf.set_font("Arial", size = 15)
        pdf.cell(50, 8, txt = self.INVOICE_NUMBER, ln = 17, align = 'L')

        pdf.output("MobiDuniya-Invoice-"+self.INVOICE_NUMBER+".pdf")

        return "MobiDuniya-Invoice-"+self.INVOICE_NUMBER+".pdf"

