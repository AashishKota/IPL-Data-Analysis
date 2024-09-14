import requests
from bs4 import BeautifulSoup
import scrape_overs
import scrape_match
import re
DIM_PLAYERS = './ipl/dim_players.csv'
BATTING_PATH = './ipl/batting_stats.csv'
BOWLING_PATH = './ipl/bowling_stats.csv'
DIM_MATCHES = './ipl/match_summary.csv'
OVERS = './ipl/overs.csv'
SERIES_ID = '2024-1410320'
headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36'
}
print(0)

#main_page = requests.get("https://webcache.googleusercontent.com/search?q=cache:https://www.espncricinfo.com/series/indian-premier-league-"+SERIES_ID+"/match-schedule-fixtures-and-results",headers=headers)
main_page = requests.get("https://www.espncricinfo.com/series/indian-premier-league-"+SERIES_ID+"/match-schedule-fixtures-and-results",headers=headers)
soup = BeautifulSoup(main_page.text,'html5lib')
#list = soup.findAll('div',class_='ds-p-4 ds-border-y ds-border-line')
#list = soup.findAll('div',class_='ds-p-4 hover:ds-bg-ui-fill-translucent')
list = soup.select('div.ds-p-4.hover\\:ds-bg-ui-fill-translucent.ds-border-none.ds-border-t.ds-border-line, div.ds-p-4.hover\\:ds-bg-ui-fill-translucent')

i=0
#print(soup)
print(len(list))

for li in list:
    te = li.find('a')
    ur = re.search('.*-(.*)/full-scorecard',te['href']).group(1)
    #print(te['href'])
    if ur.split('-')[-1]>='0000000':
        overs_url = 'https://hs-consumer-api.espncricinfo.com/v1/pages/match/overs/details?lang=en&seriesId='+SERIES_ID.split('-')[-1]+'&matchId='+ur.split('-')[-1]+'&mode=ALL'
        print(ur)
        scrape_overs.overs(overs_url,ur)

        #if ur > '1298155':
        match_url = 'https://hs-consumer-api.espncricinfo.com/v1/pages/match/scorecard?lang=en&seriesId='+SERIES_ID.split('-')[-1]+'&matchId='+ur.split('-')[-1]
        scrape_match.match(match_url)
        i+=1
    
print(main_page.status_code)
print(len(list))
#with open('temp.html','wb') as f:
#    f.write(soup.prettify().encode('utf-8'))
