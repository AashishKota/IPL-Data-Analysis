import csv
import json
import requests
OVERS = './ipl/overs.csv'

def overs(url,ur):
    # Load the JSON file
    #print(url)
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.79 Safari/537.36'
    }
    data = requests.get(url,headers=headers)
    #print(data.status_code)
    data = data.json()
    #data = json.loads(f)
    with open('temp4.json','w') as f:
        json.dump(data,f,indent=4)
    #for i,j in data.items():
    #    print(i)
    rows=[]
    # Extract the overs by batting and bowling data from the JSON file
    for inningss in [0,1]:
        try:
            bdata = data['inningOvers'][inningss]
        except:
            break
        # Create a list of dictionaries to hold the extracted data
        #rows = []

        #inningOvers[0].stats[0].balls  inningOvers[1].stats[3].bowlers[0].longName
        # Iterate over the bowling data and create a dictionary for each ball
        i=1
        for over in bdata['stats']:
            i+=1
            for ball in over['balls']:
                ball_data = {
                    'matchId': ur,
                    'over': over['overNumber'],
                    'bowler': over['bowlers'][0]['longName'],
                    'batsmanPlayerId': ball["batsmanPlayerId"],
                    "bowlerPlayerId": ball["bowlerPlayerId"],
                    'inningNumber': ball["inningNumber"],
                    'oversUnique': ball["oversUnique"],
                    "oversActual": ball["oversActual"],
                    "totalRuns": ball["totalRuns"],
                    "batsmanRuns": ball["batsmanRuns"],
                    "isFour": ball["isFour"],
                    "isSix": ball["isSix"],
                    "isWicket": ball["isWicket"],
                    "byes": ball["byes"],
                    "legbyes": ball["legbyes"],
                    "wides": ball["wides"],
                    "noballs": ball["noballs"],
                }
                rows.append(ball_data)
        #print(len(rows))
    if len(rows)<=0:
        return
    # Write the extracted data to a CSV file
    with open(OVERS, 'a+', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        cur_pos = f.tell()
        start = f.seek(0)
        if start==cur_pos:
            writer.writeheader()
        writer.writerows(rows)
