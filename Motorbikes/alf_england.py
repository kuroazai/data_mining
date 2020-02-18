# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 14:43:10 2020

@author: fidelismwansa
"""


from bs4 import BeautifulSoup
import urllib3
import re
urllib3.disable_warnings()
http = urllib3.PoolManager()


def get_prices(soup):
    # Fine the price
    divs = soup.findAll("div", {"class": "grid-container"})
    span = re.findall('"bike-price">([^"]*)<', str(divs))
    price = re.sub('\D', '', span[0])
    price = price[:-3]
    price = price[1-len(price):]
    print "Price : £", price

    # Find specs
    specs = soup.findAll("div", {"class": "bike-specification"})
    #specs = list(filter(None, specs))    
    #specs = [x for x in specs if x]
    i = 0
    e_specs = []
    for x in specs[0]:
        if None == x.name:
            pass
        else:
            #print i, x, "\n"
            e_specs.append(x)
            i += 1
    #print len(e_specs)
    # Find Weight
    span = re.findall('>([^"]*)kg', str(specs))
    print "Weight : ", span[len(span)-1].strip(), "KG"
    # Find Horsepower & Peak Power
    m_hp = re.findall('(kW ([^"]*)) @', str(e_specs[4]))

    if len(m_hp) >= 1:
        a = str(m_hp[0]).split(",")
        a = re.sub('\D', '', a[1])
        m_hp = re.sub('\D', '', str(m_hp[0]))
        #print a[:-1], len(a)
        m_hp = m_hp[:len(m_hp) / 2 + 1]
        if len(a) > 2:
            hp = float(a[:-1]) / 1.014
        else:
            hp = float(a) / 1.014

        print "Horse Power : ", "{:.2f}".format(hp), "HP"
        peak_p = re.findall('(@([^"]*))rpm', str(e_specs[4]))
        a = str(peak_p[0]).split()
        print "Peak Power @ ", a[1], "RPM"
        m_hp = re.sub('\D', '', str(m_hp[0]))
    else:
        print "Horsepower Unavaliable"

    #Find Displacement 
    dpc = re.findall('>([^"]*)cc', str(e_specs[1]))
    print "Displacement : ", dpc[0], "CC"
    
    #Find Torque & peak
    trq = re.findall('>([^"]*) Nm', str(e_specs[5]))
    if len(trq) >= 1:    
        print "Torque : ", trq[0], "Nm"
        peak_t = re.findall('(@([^"]*))rpm', str(e_specs[5]))   
        b = str(peak_t[0]).split()
        print "Peak Torque @ ", b[1], "RPM"
    else:
        print "Torque Unavaliable"
def save():
    pass


# Individual Containers for the names of the bikes
Yzf = ['yzf-R1M', 'yzf-R1', 'yzf-R6', 'yzf-R3', 'yzf-R125']
Mt = ['MT-10-SP', 'MT-10', 'MT-07', 'MT-03', 'MT-125']

# Joint container
bikes = Yzf + Mt

# base url
url = "https://www.alfengland.co.uk/new-yamaha-bikes/asset/" + bikes[4]
#********************************************************************
#   Beautiful Soup
#********************************************************************
response = http.request('GET', url)
soup = BeautifulSoup(response.data, "html.parser")

for x in bikes:
    print x

    # Build Url
    url = "https://www.alfengland.co.uk/new-yamaha-bikes/asset/" + x
    print url
    # Soup
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data, "html.parser")
    get_prices(soup)
    print "\n\n"

raw_input()

