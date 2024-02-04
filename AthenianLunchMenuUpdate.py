import io
import os
from datetime import date;
import requests
from bs4 import BeautifulSoup
from PyPDF2 import PdfReader, PdfWriter
from urllib.request import Request, urlopen

#https://stackoverflow.com/questions/16627227/problem-http-error-403-in-python-3-web-scraping

url = "https://www.athenianschooldining.com/"

req = Request(url, headers={'User-Agent': 'XYZ/3.0'})
webpage = urlopen(req, timeout=10).read()
soup = BeautifulSoup(webpage, 'html.parser')
#print(soup.prettify())
MENU_LINKS = soup.find_all("a", "elementor-button elementor-button-link elementor-size-xl elementor-animation-float", limit=2)
DATES = soup.find_all("h2", "elementor-heading-title elementor-size-default", limit=2)


def getStartDay(string):
    string = string[0: string.index('-')]
    return int(string[string.index('/') + 1:len(string)])


def getStartMonth(string):
    string = string[0: string.index('-')+1]
    return int(string[0: string.index('/')])


def getEndDay(string):
    string = string[string.index('-'):len(string)]
    return int(string[string.index('/') + 1:len(string)])


def getEndMonth(string):
    string = string[string.index('-'):len(string)]
    return int(string[1])


LINK_1 = MENU_LINKS[0].get('href')
LINK_2 = MENU_LINKS[1].get('href')
LINK_1_DATE = DATES[0].text
LINK_2_DATE = DATES[1].text

month = date.today().month
day = date.today().day
weekday = date.today().weekday()


LINK = "null"
'''
print(getStartDay(LINK_2_DATE))
print(getStartMonth(LINK_2_DATE))
print(getEndDay(LINK_2_DATE))
print(getEndMonth(LINK_2_DATE))

print("Day: " + str(day))
print ("Month: " + str(month))
'''
if getStartDay(LINK_1_DATE)<=day and day<=getEndDay(LINK_1_DATE):
    LINK = LINK_1
elif month > getStartMonth(LINK_1_DATE) and month == getEndMonth(LINK_1_DATE):
    if day<getEndDay():
        LINK = LINK_1
elif getStartDay(LINK_2_DATE)<=day and day<=getEndDay(LINK_2_DATE):
    LINK = LINK_2
elif month > getStartMonth(LINK_2_DATE) and month == getEndMonth(LINK_2_DATE):
    if(day<getEndDay(LINK_2_DATE)):
        LINK = LINK_2

print(LINK)
print(date.today().weekday())

headers = {'User-Agent': 'Mozilla/5.0 (X11; Windows; Windows x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36'}

req = Request(LINK, headers={'User-Agent': 'XYZ/3.0'})
response = requests.get(url=LINK_1, headers=headers, timeout=120)
on_fly_mem_obj = io.BytesIO(urlopen(req, timeout=10).read())
pdf = PdfReader(on_fly_mem_obj)

print(len(pdf.pages))
writer = PdfWriter()
page = pdf.pages[0]
y4 = 0
y5 = 0

if weekday == 0:  # Monday
    y4 = 415  # top left
    y5 = 690  # bottom right

elif weekday == 1:  # Tuesday
    y4 = 663  # top left
    y5 = 940  # bottom right

elif weekday == 2:  # Wednesday
    y4 = 913  # top left
    y5 = 1222  # bottom right

elif weekday == 3:  # Thursday
    y4 = 1187  # top left
    y5 = 1486  # bottom right

elif weekday == 4:  # Friday
    y4 = 1460  # top left
    y5 = 1744  # bottom right

elif weekday == 5:  # Saturday
    y4 = 1730  # top left
    y5 = 1900  # bottom right

elif weekday == 6:  # Sunday
    y4 = 1890  # top left
    y5 = 2084  # bottom right


page.cropbox.upper_left = (612*(70)/(1700),(1-y4/2200)*792)
page.cropbox.lower_right = (612*(1510)/(1700),(1-y5/2200)*792)
writer.add_page(page)

with open(os.path.join('C:/Users/willi/Desktop/Athenian Lunch Menu/file.pdf'),'wb') as fp:
    writer.write(fp)

print(page.cropbox.lower_left)
print(page.cropbox.lower_right)
print(page.cropbox.upper_left)
print(page.cropbox.upper_right)
