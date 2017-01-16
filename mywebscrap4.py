from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv
import time

type1 = 'Retail price of farm crops and animal feed'
category = 'Farm Plants'
product = 'Black bean'


url = 'http://www.dit.go.th/en/PriceStat.aspx'

with requests.Session() as session:
    session.headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
        'X-Requested-With': 'XMLHttpRequest'
    }
    response = session.get(url)
    soup = BeautifulSoup(response.content)

# build an options mapping
options1 = {option.get_text(strip=True): option['value'] for option in soup.select("select#ctl00_MainContent_ddl_type option")[1:]}
options2 = {option.get_text(strip=True): option['value'] for option in soup.select("select#ctl00_MainContent_ddl_category option")[1:]}
options3 = {option.get_text(strip=True): option['value'] for option in soup.select("select#ctl00_MainContent_ddl_product option")[1:]}

    # parse form parameters
form = soup.find("form", id="aspnetForm")
params = {
        '__EVENTTARGET': form.find('input', {'name': '__EVENTTARGET'})['value'],
        '__EVENTARGUMENT': form.find('input', {'name': '__EVENTARGUMENT'})['value'],
        '__LASTFOCUS': form.find('input', {'name': '__LASTFOCUS'})['value'],
        '__VIEWSTATE': form.find('input', {'name': '__VIEWSTATE'})['value'],
        '__VIEWSTATEGENERATOR': form.find('input', {'name': '__VIEWSTATEGENERATOR'})['value'],
        '__EVENTVALIDATION': form.find('input', {'name': '__EVENTVALIDATION'})['value'],
        'ctl00$MainContent$ddl_product': options3.get(product),
        'ctl00$MainContent$ddl_category': options2.get(category),
        'ctl00$MainContent$ddl_type': options1.get(type1),
        'ctl00$MainContent$hd_unit': 'NULL'
    }

response = session.post(url, data=params)

    # parse the results
soup = BeautifulSoup(response.content)


#for row in soup.find_all('tr'):
#    cells=row.find_all("td")
#    print(cells)
'''
for row in soup.select('table#MainContent_gv1 tr')[1:]:
  for x in range(0, 12):
     print (row.find_all("td")[x].text)
'''
data = {
    'year' : [],
    '1' : [],
    '2' : [],
    '3' : [],
    '4' : [],
    '5' : [],
    '6' : [],
    '7' : [],
    '8' : [],
    '9' : [],
    '10' : [],
    '11' : [],
    '12' : [],
}

for row in soup.select('table#ctl00_MainContent_gv1 tr')[1:]:
    cols = row.find_all('td')
    data['year'].append( cols[0].get_text() )
    data['1'].append( cols[1].get_text() )
    data['2'].append( cols[2].get_text() )
    data['3'].append( cols[3].get_text() )
    data['4'].append( cols[4].get_text() )
    data['5'].append( cols[5].get_text() )
    data['6'].append( cols[6].get_text() )
    data['7'].append( cols[7].get_text() )
    data['8'].append( cols[8].get_text() )
    data['9'].append( cols[9].get_text() )
    data['10'].append( cols[10].get_text() )
    data['11'].append( cols[11].get_text() )
    data['12'].append( cols[11].get_text() )

dogData = pd.DataFrame( data )
#print dogData.values
new_header = dogData.iloc[0] #grab the first row for the header
#dogData = dogData[1:] #take the data less the header row
dogData.rename(columns = new_header) #set the header row as the df header

dogData = dogData[['year', '1', '2','3', '4','5','6','7','8','9','10','11','12']]
cols = list(dogData.columns.values)
#dogData = dogData.drop(dogData.columns[0], axis=1)

dogData = pd.melt(dogData, id_vars=['year'], value_vars=['1', '2','3', '4','5','6','7','8','9','10','11','12'], var_name="month", value_name = "price")
timestr = time.strftime("%Y%m%d_")
filename='{0},{1},{2}'.format(timestr,product,".csv")
dogData.to_csv(filename, header=True, index=False)
