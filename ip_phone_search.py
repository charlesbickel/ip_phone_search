import re
import requests
import csv
import textMyself
from netaddr import *


ip_phone = 0
match_phones = 0

iprange = (IPRange('beginning range', 'end range'))


for ip in iprange:
    try:
        r = requests.get('http://' + str(ip), timeout=0.5)

        print('---------------')
        print(ip)
        print(r.status_code)
        print('---------------')

        if r.status_code == 200:
            verify_cisco = re.compile(r'(ip phone)', re.I)  # See if 'IP Phone' is on the page (Ignore case)
            mo = verify_cisco.search(r.text)
            print('*** I found one! ' + mo.group())
            ip_phone += 1

            if mo is not None:
                typeRegex = re.compile(r'(7942G|7962G|7911|7925)')  # Filtering out only 7942Gs,7962Gs, 7911s,7925s
                mo2 = typeRegex.search(r.text)
                match_phones += 1

                if mo2 is not None:
                    print(mo2.group())
                    serialRegex = re.compile(r'FCH(\w){8}')  # Find Serial Number
                    serial = serialRegex.search(r.text)
                    print(serial.group())

                    with open('IP_Phones.csv', 'a') as f:  # Saving serials in a csv
                        writer = csv.writer(f, delimiter='|', lineterminator='\n')
                        writer.writerow([serial.group()])

    except Exception as err:
        'There was an error'

textMyself.textmyself('The task completed. ' +
                      ip_phone + ' IP phones. ' +
                      match_phones + ' matching phones.')
