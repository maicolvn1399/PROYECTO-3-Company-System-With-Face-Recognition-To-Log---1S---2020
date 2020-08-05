import requests
from datetime import date

class GetBankInformation:
    def __init__(self):
        self.today = date.today()#set up today's date
        self.date = self.today.strftime("%d/%m/%Y")#gets today's date

        #URL which is used to get the exchange rate
        self.url = "https://gee.bccr.fi.cr/Indicadores/Suscripciones/WS/wsindicadoreseconomicos.asmx/ObtenerIndicadoresEconomicosXML"

        #Dictionary with user's information in order to get the exchange rate
        self.myInformation = {"Indicador":"317",
                             "FechaInicio":self.date,
                             "FechaFinal":self.date,
                             "Nombre":"Michael Valverde Navarro",
                             "SubNiveles":"N",
                             "CorreoElectronico":"maicolvn1399@gmail.com",
                             "Token":"VLCMA9MD2V",
                             }

    def get_my_information(self):
        """Returns information from the user that is requesting the exchange rate"""
        print(self.myInformation)
        return self.myInformation

    def getExchangeRate(self):
        """Returns the exchange rate from BCCR"""
        result = requests.post(self.url,data = self.myInformation)
        index = result.text
        cut = index.find("NUM_VALOR")
        cut2 = index.find("/NUM_VALOR")
        data = result.text[cut:cut2].replace("NUM_VALOR&gt;","").replace("&lt;","")
        print(float(data))
        return float(data)

info = GetBankInformation()
info.getExchangeRate()




