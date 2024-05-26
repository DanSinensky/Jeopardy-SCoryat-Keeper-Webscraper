from flask import Flask, jsonify, request
import json

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
        'total_pages': (len(games_data) + size - 1) // size,  # Calculate total pages
        'games': paginated_games
    }

    return jsonify(response)

@app.route('/api/games/<int:game_id>', methods=['GET'])
def get_game_by_id(game_id):
    for game in games_data:
        if 'error' not in game and game['game_title'].endswith(str(game_id)):
            return jsonify(game)
    return jsonify({'error': f'Game {game_id} not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
