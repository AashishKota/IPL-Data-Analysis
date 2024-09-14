import csv
import json
import requests
import pandas as pd

DIM_PLAYERS = './ipl/dim_players.csv'
BATTING_PATH = './ipl/batting_stats.csv'
BOWLING_PATH = './ipl/bowling_stats.csv'
DIM_MATCHES = './ipl/match_summary.csv'

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36'
}

def player_data(id):
    #url = 'https://hs-consumer-api.espncricinfo.com/v1/pages/player/stats?playerId={}'.format(id)
    url = 'https://hs-consumer-api.espncricinfo.com/v1/pages/player/home?playerId={}'.format(id)
    data = requests.get(url,headers=headers)
    print(data.status_code,id)
    data = data.json()
    player_info = {
        "objectId": data['player']['objectId'],
		"longName": data['player']['longName'],
		"battingName": data['player']['battingName'],
		"slug": data['player']['slug'],
		"imageUrl": data['player']['imageUrl'],
		"fieldingName": data['player']['fieldingName'],
		"gender": data['player']['gender'],
		"playingRole": data['player']['playingRoles'],
		"longBattingStyles": data['player']['longBattingStyles'],
		"longBowlingStyles": data['player']['longBowlingStyles'],
        "country" : data['player']['country']['name']
    }
    #print(player_info,type(player_info))
    with open(DIM_PLAYERS,'a+',encoding='utf-8',newline='') as f:
        writer = csv.DictWriter(f, fieldnames=player_info.keys())
        cur_pos = f.tell()
        start = f.seek(0)
        if start==cur_pos:
            writer.writeheader()
        writer.writerow(dict(player_info))

def batting_stats(data):
    inning = data['content']['innings']
    #player_info = pd.read_csv(DIM_PLAYERS)
    rows = []
    flag=True
    if len(inning)==0:
        return
    for i in range(len(inning)):
        for j in range(0,11):
            batsman_data = {}
            batsman = inning[i]['inningBatsmen']
            id = batsman[j]['player']['objectId']
            if batsman[j]['battedType']=="no":
                continue
            batsman_data = {
                "matchId" : data['match']['objectId'],
                "slug" : batsman[j]['player']['slug'],
                "playerid" : batsman[j]['player']['objectId'],
                "runs": batsman[j]['runs'],
                "balls": batsman[j]['balls'],
                "minutes": batsman[j]['minutes'],
                "fours": batsman[j]['fours'],
                "sixes": batsman[j]['sixes'],
                "strikerate": batsman[j]['strikerate'],
                "isOut": batsman[j]['isOut']
            }
            rows.append(batsman_data)
            if flag:
                player_data(batsman_data['playerid'])
                flag=False
            player_info = pd.read_csv(DIM_PLAYERS)
            if batsman_data['playerid'] not in set(player_info['objectId']):
                player_data(batsman_data['playerid'])
    #print(4)
    with open(BATTING_PATH, 'a+', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        cur_pos = f.tell()
        start = f.seek(0)
        if start==cur_pos:
            writer.writeheader()
        writer.writerows(rows)

    #print('1')

def bowling_stats(data):
    inning = data['content']['innings']
    player_info = pd.read_csv(DIM_PLAYERS)
    rows = []
    if len(inning)==0:
        return
    for i in range(len(inning)):
        bowlers = inning[i]['inningBowlers']
        for j in range(len(bowlers)):

            if bowlers[j]['player']['objectId']=="no":
                continue
            id = bowlers[j]['player']['objectId']
            bowler_data = {
                "matchId" : data['match']['objectId'],
                "slug" : bowlers[j]['player']['slug'],
                "playerid" : bowlers[j]['player']['objectId'],
                "overs": bowlers[j]['overs'],
                "balls": bowlers[j]['balls'],
                "maidens": bowlers[j]['maidens'],
                "conceded": bowlers[j]['conceded'],
                "wickets": bowlers[j]['wickets'],
                "economy": bowlers[j]['economy'],
                "runsPerBall": bowlers[j]['runsPerBall'],
                "dots": bowlers[j]['dots'],
                "fours": bowlers[j]['fours'],
                "sixes": bowlers[j]['sixes'],
                "wides": bowlers[j]['wides'],
                "noballs": bowlers[j]['noballs'],
            }
            rows.append(bowler_data)
            
            player_info = pd.read_csv(DIM_PLAYERS)
            if bowler_data['playerid'] not in set(player_info['objectId']):
                player_data(bowler_data['playerid'])
    with open(BOWLING_PATH, 'a+', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        cur_pos = f.tell()
        start = f.seek(0)
        if start==cur_pos:
            writer.writeheader()
        writer.writerows(rows)

    #print('2')

def match_summary(data):
    data = data['match']
    match_info = {
        'matchId' : data['objectId'],
        'name' : data['slug'],
        'result' : data['statusText'],
        'winnerId' : data['winnerTeamId'],
        'team_1' : data['teams'][0]['team']['objectId'],
        'team1Name' : data['teams'][0]['team']['longName'],
        'team_2' : data['teams'][1]['team']['objectId'],
        'team2Name' : data['teams'][1]['team']['longName'],
    }
    print(match_info['name'],match_info['result'])
    with open(DIM_MATCHES, 'a+', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=match_info.keys())
        cur_pos = f.tell()
        start = f.seek(0)
        if start==cur_pos:
            writer.writeheader()
        writer.writerow(match_info)

def match(url):
    #print(url)
    data = requests.get(url,headers=headers)
    #print(data.status_code)
    data = data.json()
    with open('temp5.json','w') as f:
        json.dump(data,f)
    #print(1)
    match_summary(data)
    #print(2)
    batting_stats(data)
    #print(3)
    bowling_stats(data)