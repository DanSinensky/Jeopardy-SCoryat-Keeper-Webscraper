from flask import Flask, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

def scrapeGame():
  pageToScrape = requests.get('https://j-archive.com/showgame.php?game_id=8792')
  soup = BeautifulSoup(pageToScrape.text, "html.parser")

  game_title = soup.find('div', attrs={'id':'game_title'}).contents[0].text.strip()
  game_comments = soup.find('div', attrs={'id':'game_comments'}).text.strip()
  categories = [cat.text.strip() for cat in soup.findAll('td', attrs={'class':'category_name'})]
  category_comments = [com.text.strip() for com in soup.findAll('td', attrs={'class':'category_comments'})]

  jeopardy_clues = []
  jeopardy_responses = []
  double_jeopardy_clues = []
  double_jeopardy_responses = []

  for y in range(1,6):
    for x in range(1,7):
      clue = soup.find('td', attrs={'id': f'clue_J_{x}_{y}'})
      if clue:
        jeopardy_clues.append(clue.text.strip())

      double_clue = soup.find('td', attrs={'id': f'clue_DJ_{x}_{y}'})
      if double_clue:
        double_jeopardy_clues.append(double_clue.text.strip())
  final_jeopardy_clue = soup.find('td', attrs={'id':'clue_FJ'})
  final_jeopardy_clue_text = final_jeopardy_clue.text.strip() if final_jeopardy_clue else ""

  responses = soup.findAll('em', attrs={'class':'correct_response'})
  for count, response in enumerate(responses, start=1):
    if count < 31:
      jeopardy_responses.append(response.text.strip())
    elif 30 < count < 61:
      double_jeopardy_responses.append(response.text.strip())
    else:
      final_jeopardy_response = response.text.strip()

  return {
        'game_title': game_title,
        'game_comments': game_comments,
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


scraped_data = scrapeGame()

@app.route('/api/game_title', methods=['GET'])
def api_game_title():
    return jsonify({'game_title': scraped_data['game_title']})

@app.route('/api/game_comments', methods=['GET'])
def api_game_comments():
    return jsonify({'game_comments': scraped_data['game_comments']})

@app.route('/api/categories', methods=['GET'])
def api_categories():
    return jsonify({'categories': scraped_data['categories']})

@app.route('/api/category_comments', methods=['GET'])
def api_category_comments():
    return jsonify({'category_comments': scraped_data['category_comments']})

@app.route('/api/jeopardy_round', methods=['GET'])
def api_jeopardy_round():
    return jsonify(scraped_data['jeopardy_round'])

@app.route('/api/double_jeopardy_round', methods=['GET'])
def api_double_jeopardy_round():
    return jsonify(scraped_data['double_jeopardy_round'])

@app.route('/api/final_jeopardy', methods=['GET'])
def api_final_jeopardy():
    return jsonify(scraped_data['final_jeopardy'])

if __name__ == '__main__':
    app.run(debug=True)