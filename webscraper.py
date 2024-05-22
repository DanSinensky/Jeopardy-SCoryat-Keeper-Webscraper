from bs4 import BeautifulSoup
import requests

def scrapeGame():
  pageToScrape = requests.get('https://j-archive.com/showgame.php?game_id=8792')
  soup = BeautifulSoup(pageToScrape.text, "html.parser")
  game_title = soup.find('div', attrs={'id':'game_title'}).contents[0]
  game_comments = soup.find('div', attrs={'id':'game_comments'})
  categories = soup.findAll('td', attrs={'class':'category_name'})
  category_comments = soup.findAll('td', attrs={'class':'category_comments'})
  # clue_value = soup.findAll('td', attrs={'class':'clue_value'})

  jeopardy_clues = []
  jeopardy_responses = []
  double_jeopardy_clues = []
  double_jeopardy_responses = []

  for y in range(1,6):
    for x in range(1,7):
      clue = soup.find('td', attrs={'id': f'clue_J_{x}_{y}'})
      jeopardy_clues.append(clue)

      double_clue = soup.find('td', attrs={'id': f'clue_DJ_{x}_{y}'})
      double_jeopardy_clues.append(double_clue)
  final_jeopardy_clue = soup.find('td', attrs={'id':'clue_FJ'})

  responses = soup.findAll('em', attrs={'class':'correct_response'})
  for count, response in enumerate(responses, start=1):
    if count < 31:
      jeopardy_responses.append(response)
    elif 30 < count < 61:
      double_jeopardy_responses.append(response)
    else:
      final_jeopardy_response = response

  print(game_title.text + " - " + game_comments.text)
  for category, category_comment in zip(categories, category_comments):
    print(category.text + category_comment.text)
  for jeopardy_clue, jeopardy_response in zip(jeopardy_clues, jeopardy_responses):
    print(jeopardy_clue.text + " - " + jeopardy_response.text)
  for double_jeopardy_clue, double_jeopardy_response in zip(double_jeopardy_clues, double_jeopardy_responses):
    print(double_jeopardy_clue.text + " - " + double_jeopardy_response.text)
  print(final_jeopardy_clue.text + " - " + final_jeopardy_response.text)

scrapeGame()