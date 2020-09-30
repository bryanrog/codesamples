#Function to call a webservice repeatedly

import requests
import time
import csv
import argparse

#variables
login = '' #Ubersite login
passw = '' #ubersite password
patch = 'IQ_GEN2_WIFI_Update_2_3_4'  #'3253' #2.20T UDP  #'3094' #319 20181024
2fa = ''
filepath = "" #Where your CSV file is located on your drive
column = 0


#Function to call webservice
def fwUpdate(login, passw, 2fa, CID, patch):
    #URL endpoint for webservice, use HTTPS or you will get yelled at by NOC support
    url = 'https://alarmadmin.alarm.com/webservices/customerManagement.asmx?WSDL'
    #Heaers for SOAP calls, don't change this
    headers = {'content-type':'text/xml'}
    #Body of SOAP call, can be found at URL above. Include the variables in the places they should go.
    body = """<?xml version="1.0" encoding="utf-8"?>
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Header>
    <Authentication xmlns="http://www.alarm.com/WebServices">
      <User>"""+login+"""</User>
      <Password>"""passw"""</Password>
      <TwoFactorDeviceId>"""+2fa+"""</TwoFactorDeviceId>
    </Authentication>
  </soap:Header>
  <soap:Body>
    <RequestFirmwareUpgradeQolsys xmlns="http://www.alarm.com/WebServices">
      <customerId>"""+CID+"""</customerId>
      <newVersion>"""+patch+"""</newVersion>
      <timeToUpdate></timeToUpdate>
    </RequestFirmwareUpgradeQolsys>
  </soap:Body>
</soap:Envelope>"""

#Call the requests library to post the SOAP call and print the response and any other debug to the console
    response = requests.post(url, data = body, headers = headers)
   # print(CID)
    print(response.content)

#Open up your CSV
with open(filepath, 'rt') as csvfile:
    cidcsv = csv.reader(csvfile, delimiter = ',')

    #Loop through CSV rows
    for row in cidcsv:
        fwUpdate(login, passw, 2fa, row[column], patch)
        time.sleep(6)




print("Done")
    
