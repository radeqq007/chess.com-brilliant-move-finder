import sys
import csv
import json
import re
import requests

from pprint import pprint

headers = {
    'User-Agent': 'chess-rag-cli (https://github.com/NotJoeMartinez/chess.com-brilliant-move-finder)'
}
TARGET_TIME_CLASS = "rapid"

def main():

    if len(sys.argv) < 2:
        print("Usage: python brilliant_move_finder.py <username> <time_class>")
        sys.exit(1)

    if len(sys.argv) < 3:
        print("No time class specified, using rapid")
    else:
        if sys.argv[2] not in ["bullet", "blitz", "rapid", "daily"]:
            print("Invalid time class, using rapid")
            sys.exit(1)
        global TARGET_TIME_CLASS
        TARGET_TIME_CLASS = sys.argv[2]


    username = sys.argv[1] 
    if "https://" in username:
        username = username.split('/')[-1]


    user_uuid = get_user_uuid(username)
    brilliant_dates = get_user_brilliant_dates(username, user_uuid)
    print("Fetching potential games...")
    get_potential_games(username, brilliant_dates)
    print(f"Potential games saved to {username}_potential_{TARGET_TIME_CLASS}_games.csv")


def get_potential_games(username, brilliant_dates):

    valid_games = []

    for date in brilliant_dates:

        # 2023-01-19 YYYY-MM-DD
        year = date.split('-')[0]
        month = date.split('-')[1]
        month_archive_url = f"https://api.chess.com/pub/player/{username}/games/{year}/{month}"

        r = requests.get(url=month_archive_url, headers=headers)

        if r.status_code != 200:
            print(f"Error fetching {month_archive_url}")
            continue

        games_dict = r.json()
        games_list = games_dict["games"]

        # parse the pgn element of the game node
        # unix epoch "end_time" element is unreliable because of midnight games
        for game in games_list:
            pgn = game["pgn"]

            date_match = re.search(r'\[Date\s+"([^"]+)"\]', pgn)
            if date_match:
                time_class = game["time_class"]
                date_value = date_match.group(1)

                if (date_value.replace('.', '-') == date and 
                    time_class == TARGET_TIME_CLASS):

                    game["date"] = date_value.replace('.', '-')
                    valid_games.append(game)
            else:
                print("Date not found")
                continue

            

    csv_data = []
    for game in valid_games:
        # url, user_rating, opponent_rating, result, user_accuracy, opponent_accuracy
        user_color = None
        if game["white"]["username"].lower() == username.lower():
            user_color = "white"
        else:
            user_color = "black"

        url = game["url"]
        url_id = url.split('/')[-1]
        reviewed_url = f"https://www.chess.com/analysis/game/live/{url_id}?tab=review"

        if user_color == "white":
            user_rating = game["white"]["rating"]
            opponent_rating = game["black"]["rating"]
            opponent_username = game["black"]["username"]
            result = game["white"]["result"]

            if 'accuracies' in game.keys():
                user_accuracy = game["accuracies"]["white"]
                opponent_accuracy = game["accuracies"]["black"]
            else:
                user_accuracy = '' 
                opponent_accuracy = '' 

        else:
            user_rating = game["black"]["rating"]
            opponent_rating = game["white"]["rating"]
            opponent_username = game["white"]["username"]
            result = game["black"]["result"]

            if 'accuracies' in game.keys():
                user_accuracy = game["accuracies"]["black"]
                opponent_accuracy = game["accuracies"]["white"]
            else:
                user_accuracy = '' 
                opponent_accuracy = '' 
        

        date = game["date"]
        csv_data.append({
            "brilliant": "",
            "url": reviewed_url,
            "date": date,
            "openent_username": opponent_username, 
            "user_rating": user_rating,
            "opponent_rating": opponent_rating,
            "result": result,
            "user_accuracy": user_accuracy,
            "opponent_accuracy": opponent_accuracy
        })

    # sort csv_data by user_accuracy, ignore empty values 
    csv_data = sorted(csv_data, key=lambda x: x["user_accuracy"] if x["user_accuracy"] else 0, reverse=True)

    csv_headers = ["brilliant", "url", "date", "openent_username", "user_rating", "opponent_rating",
                   "result", "user_accuracy", "opponent_accuracy"]
    with open(f"{username}_potential_{TARGET_TIME_CLASS}_games.csv", "w") as f:
        writer = csv.DictWriter(f, fieldnames=csv_headers)
        writer.writeheader()
        for row in csv_data:
            writer.writerow(row)



def get_user_brilliant_dates(username, uuid):
    url = f"https://www.chess.com/service/insights/{uuid}/{TARGET_TIME_CLASS}/all-time?uuid={uuid}"
    r = requests.get(url)

    if r.status_code == 200:
        user_data = r.json()

        # classification over time
        moves_by_classification= user_data["movesByClassificationOverTime"]

        brillant_days = []
        brilliant_count = 0
        for day in moves_by_classification.keys():
            if 'brilliant' in moves_by_classification[day]:
                brillant_days.append(day)
                brilliant_count += moves_by_classification[day]['brilliant']

        print(f"brilliant moves: {brilliant_count}")
        print(f"brilliant days: {len(brillant_days)}")
        return brillant_days



def get_user_uuid(username):
    archive_url = f"https://api.chess.com/pub/player/{username}/games/archives"
    r = requests.get(url=archive_url, headers=headers)
    month_urls = r.json()


    for url in month_urls["archives"]:
        res = requests.get(url=url, headers=headers)

        games_dict = res.json()
        games_list = games_dict["games"]

        black_username = games_list[0]["black"]["username"]

        if black_username == username:
            user_uuid = games_list[0]["black"]["uuid"]
            return user_uuid
        
        else :
            user_uuid = games_list[0]["white"]["uuid"]
            return user_uuid


if __name__ == '__main__':
    main()