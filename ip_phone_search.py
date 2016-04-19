import re
import requests
import csv
import lxml.html
import time
import textMyself
from netaddr import *


iprange = (IPRange('beginning range', 'end range'))

ip_phone = 0
match_phones = 0
start_time = time.time()


def scrape(r):
    # Parse html table into a list using xpath expressions
    doc = lxml.html.fromstring(r.text)
    stuff = (doc.xpath('.//b/text()'))

    # Use dict comprehension to convert list into dict
    d = dict([(k, v) for k, v in zip(stuff[::2], stuff[1::2])])

    # Gather the dict values into variables
    mac = (d.get(' MAC Address'))
    hname = (d.get(' Host Name'))
    serial = (d.get(' Serial Number'))
    modelnum = (d.get(' Model Number'))
    appload = (d.get(' App Load ID'))
    bootload = (d.get(' Boot Load ID'))
    hdware = (d.get(' Hardware Revision'))

    # Write data to csv file
    with open('IP_Phones.csv', 'a', newline='') as f:
        more_data = [ip, mac, hname, serial, modelnum, appload, bootload, hdware]
        writer = csv.writer(f)
        writer.writerow(more_data)

    # Sanity check
    print(stuff)


for ip in iprange:
    try:
        r = requests.get('http://' + str(ip), timeout=0.5)

        print('---------------')
        print(ip)
        print(r.status_code)
        print('---------------')

        # If the response is OK,
        # then search for 'IP phone' via regular expressions
        if r.status_code == 200:
            verify_cisco = re.compile(r'(ip phone)', re.I)
            mo = verify_cisco.search(r.text)
            print('Cisco ' + mo.group())
            ip_phone += 1

            if mo is not None:
                # If 'ip phone' found,
                # filter out only these models
                typeRegex = re.compile(r'(7942G|7962G|7911G|7925G)')
                mo2 = typeRegex.search(r.text)

                if mo2 is not None:
                    # Model above found
                    print('***FOUND ONE!***')
                    match_phones += 1
                    scrape(r)

    except Exception as err:
        'There was an error'


scan_time = round(time.time() - start_time)
print('The scan took', scan_time, 'seconds to run.')
print(ip_phone, 'IP phones.')
print(match_phones, 'Matching phones.')

textMyself.textmyself('The task completed.{}IP phones. {} matching phones. '
                      'The scan took {} seconds to run.'.format(ip_phone,
                      match_phones, scan_time))
