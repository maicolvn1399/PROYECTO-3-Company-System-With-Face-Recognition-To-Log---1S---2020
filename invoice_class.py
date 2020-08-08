from reportlab.pdfgen import canvas
from pyinvoice.models import InvoiceInfo, ServiceProviderInfo, ClientInfo, Item, Transaction
from pyinvoice.templates import SimpleInvoice
from datetime import datetime, date,timedelta
import os,shutil
import sqlite3

import random


class Invoice:
    def __init__(self,invoiceNumber,invoiceName,invoiceAddress,invoiceID,invoiceEmail,invoiceDate,invoiceExpiringDate,invoiceService):
        self.invoiceNum = invoiceNumber
        self.invoiceNumber = self.invoiceNum
        self.invoiceName = invoiceName
        self.invoiceAddress = invoiceAddress
        self.invoiceID = invoiceID
        self.invoiceEmail = invoiceEmail
        self.invoiceDate = invoiceDate
        self.invoiceExpiringDate = invoiceExpiringDate
        self.invoiceService = invoiceService

    def generateInvoice(self):
        doc = SimpleInvoice(self.invoiceName + " - " + str(self.invoiceNumber) + ".pdf")
        #Paid stamp
        doc.is_paid = False

        doc.invoice_info = InvoiceInfo(1023, datetime.now(), datetime.today() + timedelta(days=3))

        #Service provider
        doc.service_provider_info = ServiceProviderInfo(
            name= "Jardineria",
            street = "My street",
            city = "My City",
            state = "My State",
            country= "Costa Rica",
            post_code = "22222222",
            vat_tax_number = "Vat/Tax number"
        )

        #client info
        doc.client_info = ClientInfo(email=self.invoiceEmail)

        #add item
        doc.add_item(Item("Item","Item Description",1,"1.1"))


        #tax rate
        doc.set_item_tax_rate(20)

        #transactions detail
        doc.add_transaction(Transaction("Paypal",111,datetime.now(),1))
        doc.add_transaction(Transaction('Stripe', 222, date.today(), 2))

        #Optional
        doc.set_bottom_tip("Email: RMtech@gmail.com<br />Don't hesitate to contact us for any questions.")


        doc.finish()
        print("PDF Done")

    def moveInvoices(self):
        for subdir, dirs, files in os.walk(r'C:\Users\Michael\Desktop\PROYECTO 3 - Company System With Face Recognition To Log - 1S - 2020\PROYECTO-3-Company-System-With-Face-Recognition-To-Log---1S---2020'):
            for filename in files:
                filepath = subdir + os.sep + filename

                if filepath.endswith(".pdf"):
                    print(filename)
                    destination = "invoices"
                    shutil.move(filepath, destination)
                    print("Invoices moved")












