from flask import Flask, jsonify
import json

app = Flask(__name__)

with open('jeopardy_games.json', 'r') as f:
    games_data = json.load(f)

@app.route('/api/games', methods=['GET'])
def get_all_games():
    return jsonify(games_data)

@app.route('/api/games/<int:game_id>', methods=['GET'])
def get_game_by_id(game_id):
    for game in games_data:
        if 'error' not in game and game['game_title'].endswith(str(game_id)):
            return jsonify(game)
    return jsonify({'error': f'Game {game_id} not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
