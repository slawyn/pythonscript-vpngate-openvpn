import urllib2
import sys
import time
import base64
from subprocess import call

from BeautifulSoup import BeautifulSoup
VPN_GATE="http://www.vpngate.net/api/iphone/"
FILE_NAME="csvlist"
def process_csvlist():
    ovpn=[]
    headers=[]
    vpn = []
    headers_found=False
    with open(FILE_NAME) as f:

        for line in f:

            if headers_found:
                temp = line.split(",")
                vpn.append(temp[:len(temp)-1])
                encoded = temp[len(temp)-1].rstrip('\r\n')
                data = base64.b64decode(encoded)
                ovpn.append(data)
            elif  line[0:1] =="#":
                headers_found=True
                headers = line[1:].rstrip('\r\n').split(",")

    f.close()
    return headers, vpn, ovpn
def print_formated_line(num, list):
    line = "("+str(num)+")\t"
    for item in list:
        line=line+"\t"+item
    print line

def choose_vpn(headers, vpn, ovpn):
    against_dns_leak= "script-security 2\nup /etc/openvpn/update-resolv-conf\ndown /etc/openvpn/update-resolv-conf\n"
    while(True):
        line="Number\t"
        for item in headers:
            line=line+"\t"+item
        print line

        for i in range(len(vpn)):
            print_formated_line(i,vpn[i])

        value= input("Please select vpn server 0 - "+str(len(vpn)-1) +":")
        filename= vpn[value][0]
        f = open(filename,'w')
        f.write(ovpn[value])
        f.write(against_dns_leak)
        f.close()
        call(['sudo','openvpn', '--config',filename])
    return



if len(sys.argv)>1:
    if sys.argv[1] == "update":

        try:
            f = open(FILE_NAME, 'w')
            print "Fetching csvlist..."
            page = urllib2.urlopen(VPN_GATE)
            soup = BeautifulSoup(page)

            print "Writing csvlist"
            f.write("Updated on " +time.strftime("%H:%M:%S %d/%m/%Y")+"\n")

            f.write(str(soup))

        except:
            print "Unexpected Error:" + str(sys.exc_info()[0])
        f.close()

    elif sys.argv[1] == "config":
        headers, vpn, ovpn = process_csvlist()
        choose_vpn(headers, vpn, ovpn)

else:
    print "Usage: vpnscript.py <option>\noptions:\n\tupdate - downloads csvlist\n\tconfigure - configures vpn"
