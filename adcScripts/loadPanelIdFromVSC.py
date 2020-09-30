#Function to call a webservice repeatedly

import requests
from datetime import datetime
import csv
import argparse
import getpass
import time

#variables
login = input("Enter your login name: ")
passw = getpass.getpass("Enter your password: ")
#tfa = input("Enter your 2 factor authentication token (leave blank if not enabled: ")
#panelid = input("Enter panel ID list separated by commas: ")
filepath = "C:/Users/brogers/Desktop/PM360BulkLoad.txt" #Where your CSV file is located on your drive


#Function to call webservice
def loadRecord(login, passw, panelid):
    #URL endpoint for webservice, use HTTPS or you will get yelled at by NOC support
    url = 'https://alarmadmin.alarm.com/webservices/Manufacturing.asmx?WSDL'
    #Heaers for SOAP calls, don't change this
    headers = {'content-type':'text/xml'}
    #Body of SOAP call, can be found at URL above. Include the variables in the places they should go.
    body = """<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Header>
    <Authentication xmlns="http://www.alarm.com/WebServices">
      <User>"""+login+"""</User>
      <Password>"""+passw+"""</Password>
      <TwoFactorDeviceId></TwoFactorDeviceId><!--Optional:-->
    </Authentication>
  </soap:Header>
  <soap:Body>
    <ModemsTested_v3 xmlns="http://www.alarm.com/WebServices">
      <modemTestResults>
		<ModemTestResultV3>
				  <webServiceClient>1</webServiceClient>
				  <firmwareVersion>28011920</firmwareVersion> 
				  <cellRadioPresent>true</cellRadioPresent>
				  <modemInfo>
					<imei>VISONICPM"""+panelid+"""</imei> 
					<imsi></imsi> 
					<iccid></iccid>

				  </modemInfo>
				  <ethernetPresent>true</ethernetPresent>
				  <ethernetInfo>
					<macAddress>string</macAddress>
					<ethStackVersion>0</ethStackVersion> 
				  </ethernetInfo>
				  <zwaveBuiltIn>true</zwaveBuiltIn>
				  <zwaveInfo>
					<chipBinary>6.81</chipBinary> 
					<adcZwaveStackVersion>3.25</adcZwaveStackVersion> 
				  </zwaveInfo>
				  <boltBuiltIn>false</boltBuiltIn>
				   <hardwareFlavor>118</hardwareFlavor> 
				   <moduleCpu>Other</moduleCpu> 
				  <testInfo>
					<testDateTime>2019-11-04T12:52:30</testDateTime> 

				  </testInfo>
				  <testResults>
					<batteryVoltage>1200</batteryVoltage> 
					<signalLevel>0</signalLevel> 
					<ledsTested>1</ledsTested> 
					<twoWayVoiceTested>false</twoWayVoiceTested>
				  </testResults>
				 
				</ModemTestResultV3>
		</modemTestResults>
	</ModemsTested_v3>
</soap:Body>
</soap:Envelope>"""

#Call the requests library to post the SOAP call and print the response and any other debug to the console
    response = requests.post(url, data = body, headers = headers)
   # print(CID)
    output = str(response.content)
    output = output.replace('<', '')
    output = output.replace('/','>')
    parse = output.split('>')
    try:
        success = parse.index("Success")
        imei = parse[parse.index("Imei")+1]

        print(imei + " Loaded successfully")
    except ValueError:
        error = parse[parse.index("faultstring") +1]
        print(str(panelid) + " Failed to load. Error is: " + error)
        
with open(filepath, 'rt') as csvfile:
    cidcsv = csv.reader(csvfile, delimiter = ',')

    #Loop through CSV rows
    for row in cidcsv:
        print(row)
        loadRecord(login, passw, row[7])
        time.sleep(3)
##
##panels = panelid.split(' ')
##print(panels)
##for p in panels:
##    print(p)
##    loadRecord(login, passw, p)
