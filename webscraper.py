from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

def scrapeGame(game_id):
    url = f'https://j-archive.com/showgame.php?game_id={game_id}'
    pageToScrape = requests.get(url)
    
    if pageToScrape.status_code != 200:
        return {'error': 'Game not found or unable to retrieve the page'}

    soup = BeautifulSoup(pageToScrape.text, "html.parser")

    game_title = soup.find('div', attrs={'id': 'game_title'})
    game_title_text = game_title.get_text(strip=True) if game_title else "Title not found"

    game_comments = soup.find('div', attrs={'id': 'game_comments'})
    game_comments_text = game_comments.get_text(strip=True) if game_comments else "Comments not found"

    categories = [cat.get_text(strip=True) for cat in soup.findAll('td', attrs={'class': 'category_name'})]
    category_comments = [com.get_text(strip=True) for com in soup.findAll('td', attrs={'class': 'category_comments'})]

    jeopardy_clues = []
    jeopardy_responses = []
    double_jeopardy_clues = []
    double_jeopardy_responses = []

    for y in range(1, 6):
        for x in range(1, 7):
            clue = soup.find('td', attrs={'id': f'clue_J_{x}_{y}'})
            if clue:
                jeopardy_clues.append(clue.get_text(strip=True))

            double_clue = soup.find('td', attrs={'id': f'clue_DJ_{x}_{y}'})
            if double_clue:
                double_jeopardy_clues.append(double_clue.get_text(strip=True))

    final_jeopardy_clue = soup.find('td', attrs={'id': 'clue_FJ'})
    final_jeopardy_clue_text = final_jeopardy_clue.get_text(strip=True) if final_jeopardy_clue else "Final Jeopardy clue not found"

    final_jeopardy_response = "Final Jeopardy response not found"
    responses = soup.findAll('em', attrs={'class': 'correct_response'})
    for count, response in enumerate(responses, start=1):
        if count < 31:
            jeopardy_responses.append(response.get_text(strip=True))
        elif 30 < count < 61:
            double_jeopardy_responses.append(response.get_text(strip=True))
        elif count == 61:
            final_jeopardy_response = response.get_text(strip=True)

    return {
        'game_title': game_title_text,
        'game_comments': game_comments_text,
        'categories': categories,
        'category_comments': category_comments,
        'jeopardy_round': {
            'clues': jeopardy_clues,
            'responses': jeopardy_responses
        },
        'double_jeopardy_round': {
            'clues': double_jeopardy_clues,
            'responses': double_jeopardy_responses
        },
        'final_jeopardy': {
            'clue': final_jeopardy_clue_text,
            'response': final_jeopardy_response
        }
    }

@app.route('/api/scrape/<int:game_id>', methods=['GET'])
def api_scrape(game_id):
    game_data = scrapeGame(game_id)
    return jsonify(game_data)

if __name__ == '__main__':
    app.run(debug=True)
