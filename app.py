import json
import ijson
from flask import Flask, jsonify, request
import os
from apscheduler.schedulers.background import BackgroundScheduler
import atexit

app = Flask(__name__)

@app.route('/api/games', methods=['GET'])
def get_all_games():
    page = request.args.get('page', default=1, type=int)
    size = request.args.get('size', default=10, type=int)

    start = (page - 1) * size
    end = start + size

    games_data = []
    with open('jeopardy_games.json', 'r') as f:
        parser = ijson.parse(f)
        for prefix, event, value in parser:
            if prefix.endswith('.game_id'):
                if len(games_data) >= end:
                    break
                games_data.append(value)

    paginated_games = games_data[start:end]

    response = {
        'page': page,
        'size': size,
        'total_games': len(games_data),
        'total_pages': (len(games_data) + size - 1) // size,
        'games': paginated_games
    }

    return jsonify(response)

@app.route('/api/games/ids/<int:game_id>', methods=['GET'])
def get_game_by_id(game_id):
    with open('jeopardy_games.json', 'r') as f:
        games_data = json.load(f)

    for game in games_data:
        if 'error' not in game and game['game_title'].endswith(str(game_id)):
            return jsonify(game)
    return jsonify({'error': f'Game {game_id} not found'}), 404

@app.route('/api/games/date/<string:game_date>', methods=['GET'])
def get_games_by_date(game_date):
    with open('jeopardy_games.json', 'r') as f:
        games_data = json.load(f)

    games_by_date = [game for game in games_data if game.get('game_date', '').startswith(game_date)]
    
    if not games_by_date:
        return jsonify({'error': f'No games found for date {game_date}'}), 404

    return jsonify(games_by_date)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
