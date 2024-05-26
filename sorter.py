import json
from datetime import datetime

with open('jeopardy_games.json', 'r') as file:
    jeopardy_games = json.load(file)

def sort_key(entry):
    date_str = entry.get('game_date')
    if date_str:
        try:
            return (datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S"), 0)
        except ValueError:
            pass
    return (datetime.min, entry.get('game_id'))

sorted_jeopardy_games = sorted(jeopardy_games, key=sort_key)

with open('sorted_jeopardy_games.json', 'w') as json_file:
    json.dump(sorted_jeopardy_games, json_file, indent=4)

print("Data has been written to sorted_jeopardy_games.json")
