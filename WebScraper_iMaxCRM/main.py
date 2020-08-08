import requests
from bs4 import BeautifulSoup

URL = 'http://www.michric.org/member-search/21699782/0'
page = requests.get(URL)

soup = BeautifulSoup(page.content, 'html.parser')

results = soup.find(id='ResultsContainer')
#print(results.prettify())


members = results.find_all(class_='listing-details')

for member in members:
    firm = member.find('a', class_='col-sm-5')
    print(firm)
    break