#script to load PM360 test records

import requests
from datetime import datetime
import csv
import argparse
import getpass
import time
import dropbox

#variables
login = 'oemrogers' #input("Enter your login name: ")
passw = 'Password1'#getpass.getpass("Enter your password: ")
#tfa = input("Enter your 2 factor authentication token (leave blank if not enabled: ")
#panelid = input("Enter panel ID list separated by commas: ")
filepath = "C:/Users/brogers/Desktop/pm360panelid.txt" #Where your CSV file islocated on your drive
errorurl = "C:/Users/brogers/Desktop/VisonicErrors.txt"
loadids = "C:/Users/brogers/Desktop/loadedids.txt"
dbx = dropbox.Dropbox('2c6kQzAyN5AAAAAAAAAG6GdYDzh_ulhtqQkvqpA25ouqNQFiPqwe_qKErV54mZZB')



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
        with open(errorurl, 'a') as errorpath:
            errorpath.write(str(panelid) + " Failed to load. Error is: " + error+ "\n")

def download_file():
    dbx = dropbox.Dropbox('2c6kQzAyN5AAAAAAAAAG6dxUg5Ooz9YcIVIZqP4FJzii4hahB8cOHs5NDOdEFV_p')
    try:
        dbx.users_get_current_account()
    except AuthError as err:
        sys.exit("ERROR: Invalid access token")
    with open("C:/Users/brogers/Desktop/pm360panelid.txt", 'w') as f:
        metadata, res = dbx.files_download(path = "/PM360PanelIds/pm360panelid.txt")
        res = str(res.content)
        parsedres = res.split("""\\n""")
        #parsedres = parsedres.strip('\\n')
        #print("printing parsedres")
        #print(parsedres)
        for item in parsedres:
            item = item.strip('\\r')
            if len(item)>6:
                item = item.replace('VISONICPM','')
            #print(item)
            if len(item) ==6:
                
                item.upper()
                f.write(item)
                f.write('\n')
download_file()      

while True:
    idarray = []
    download_file()
    with open(loadids, 'r') as loadedids:
        try:
            
            loadedids = csv.reader(loadedids, delimiter = ',')
            #print(loadedids)
            for row in loadedids:
                #print(row[0])
                idarray.append(row[0])

            #print(idarray)
        except IndexError as err:
            print("Silly index in loaded ids")
    with open(filepath, 'rt') as csvfile:
        cidcsv = csv.reader(csvfile, delimiter = ',')

        try:
            #Loop through CSV rows
            for row in cidcsv:
                #check if Panel ID has been loaded before
                #if so, skip it
                #print( row[0])
                if row[0] in idarray:
                    #print("Already loaded")
                    pass

                 #else load it   
                else:
                    print("Printing loaded record"+row[0])
                    loadRecord(login, passw, row[0])
                    with open(loadids, 'a') as loadid:
                        loadid.write(str(row[0]) + "\n")
                                           
                    time.sleep(1)
        except IndexError as err:
            print("Too many spaces")
        csvfile.close()

        print("Going to sleep")
        time.sleep(300)
        


