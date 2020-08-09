from reportlab.pdfgen import canvas
from pyinvoice.models import InvoiceInfo, ServiceProviderInfo, ClientInfo, Item, Transaction
from pyinvoice.templates import SimpleInvoice
from datetime import datetime, date,timedelta
import os,shutil
import sqlite3

import random


class Invoice:
    def __init__(self,invoiceNumber,invoiceName,invoiceID,invoiceEmail,invoiceDate,invoiceExpiringDate,invoiceService,servicePrice,serviceDiscount,invoiceAddress):
        self.invoiceNumber = invoiceNumber
        self.invoiceName = invoiceName
        self.invoiceAddress = invoiceAddress
        self.invoiceID = invoiceID
        self.invoiceEmail = invoiceEmail
        self.invoiceDate = invoiceDate
        self.invoiceExpiringDate = invoiceExpiringDate
        self.invoiceService = invoiceService
        self.servicePrice = servicePrice
        self.serviceDiscount = serviceDiscount

    def generateInvoice(self):
        doc = SimpleInvoice(self.invoiceName + " - " + str(self.invoiceNumber) + ".pdf")
        #Paid stamp
        doc.is_paid = False

        doc.invoice_info = InvoiceInfo(self.invoiceNumber, self.invoiceDate, self.invoiceExpiringDate)

        #Service provider
        doc.service_provider_info = ServiceProviderInfo(
            name= "R&M Tech",
            street = "My street",
            city = "My City",
            state = "My State",
            country= "Costa Rica",
            post_code = "22222222",
            vat_tax_number = "Vat/Tax number"
        )

        #client info
        doc.client_info = ClientInfo(name= self.invoiceName,
                                     client_id  = self.invoiceID,
                                     email=self.invoiceEmail,
                                     street = self.invoiceAddress
                                     )

        #add item
        doc.add_item(Item(self.invoiceService,"",1,str(self.servicePrice)))



        #tax rate
        doc.set_item_tax_rate(0)

        #transactions detail
        doc.add_transaction(Transaction("Paypal",self.invoiceID,self.invoiceDate,1))

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
