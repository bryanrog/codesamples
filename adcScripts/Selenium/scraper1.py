from splinter import Browser
from time import sleep
from datetime import datetime
import csv

browser = Browser()

username = 'adcbrogers'
password = 'Sweetemotion2'

def login(username, password):

    browser.visit('https://alarmadmin.alarm.com/Default.aspx')

    browser.find_by_name('txtUsername').fill(username)
    browser.find_by_name('txtPassword').fill(password)
    browser.find_by_name('butLogin').first.click()

def changeSetting(cid):
    print('visiting : ' + 'https://alarmadmin.alarm.com/Support/RemoteToolkit.aspx?customer_id={}'.format(cid))
    browser.visit('https://alarmadmin.alarm.com/Support/RemoteToolkit.aspx?customer_id={}'.format(cid))
    browser.find_by_name('General').first.click()
    browser.find_by_name('Migration (Internal)').first.click()
    browser.find_by_name("SET MIGRATION DATE").first.click()

##def visit_extract(cid,dev_id):
##    sleep(1)
##    print('about to visit: ' + 'https://alarmadmin.alarm.com/Support/CameraInfo.aspx?customer_id={}&device_id={}'.format(cid,dev_id))
##    browser.visit('https://alarmadmin.alarm.com/Support/CameraInfo.aspx?customer_id={}&device_id={}'.format(cid[1:],dev_id))
##    print('visited')
##    browser.find_by_name('ctl00$phBody$ctl322').first.click()
##
##    sleep(15)
##
##    device_vars = browser.find_by_name('ctl00$phBody$tbCamLog').first
##
##    textblob = device_vars.text
##    #print(textblob)
##
##
##    return textblob
##
##
##def extract_memory(textblob):
##
##    standard = 'DeviceStatus.MemoryList.Memory.memoryAvailable='
##
##    interest_index = textblob.find(standard, 0)
##
##    index_of_memory = interest_index + len(standard)
##
##    data_i_need = textblob[index_of_memory:(index_of_memory + 5)]
##
##    #print('this is the interesting index {}'.format(interest_index))
##
##    #print('this is the free memory: ' + data_i_need)
##
##    return data_i_need
##
##
##def do_a_camera(cid, ded, mac):
##    textblob = visit_extract(cid, ded)
##    memory = extract_memory(textblob)
##    print('Date: {}, Time: {}, CID: {}, DED: {}, FreeMem: {}, MAC:{}'.format(datetime.today(), datetime.now(), cid, ded, memory, mac))
##
##
##def get_list():
##    with open('CamHistory.csv') as csvfile:
##        reader = csv.DictReader(csvfile, fieldnames=('cust_id','dev_id','mac'))
##        #print (reader)
##        for row in reader:
##            #(row['cust_id'], row['dev_id'], row['mac'])
##            do_a_camera(row['cust_id'], row['dev_id'], row['mac'])
##        return reader


login(username, password)

#for row in x:

#changeSetting(cid)
