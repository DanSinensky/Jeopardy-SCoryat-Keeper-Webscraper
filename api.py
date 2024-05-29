from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)

with open('jeopardy_games.json', 'r') as f:
    games_data = json.load(f)

@app.route('/api/games', methods=['GET'])
def get_all_games():
    page = request.args.get('page', default=1, type=int)
    size = request.args.get('size', default=10, type=int)

    start = (page - 1) * size
    end = start + size

    paginated_games = games_data[start:end]

    response = {
        'page': page,
        'size': size,
        'total_games': len(games_data),
        'total_pages': (len(games_data) + size - 1) // size,
        'games': paginated_games
    }

    return jsonify(response)

@app.route('/api/games/id/<int:game_id>', methods=['GET'])
def get_game_by_id(game_id):
    for game in games_data:
        if 'error' not in game and game['game_id'] == game_id:
            return jsonify(game)
    return jsonify({'error': f'Game {game_id} not found'}), 404

@app.route('/api/games/date/<string:game_date>', methods=['GET'])
def get_games_by_date(game_date):
    date_games = [game for game in games_data if game.get('game_date') and game_date in game['game_date']]
    if not date_games:
        return jsonify({'error': f'No games found for date {game_date}'}), 404
    return jsonify(date_games)

if __name__ == '__main__':
    app.run(debug=True)
