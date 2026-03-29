import requests
from bs4 import BeautifulSoup

response = requests.get('https://quotes.toscrape.com/')
if response.status_code == 200:
    #print(response.text)
    soup = BeautifulSoup(response.text, 'html.parser')
    # soup -> variable
    # soup -> response point -> filter (parser -> html)
    # parser -> html docs read / understand
    quotes = soup.find_all("span",class_="text")


    # get data from url -> soup (var) -> parser
    '''

    <html> 
    <body>
    // text
    </body>
    </html>

    '''
    # filter
    quotes = soup.select(".author")
    for q in quotes:
        print(q.text)



