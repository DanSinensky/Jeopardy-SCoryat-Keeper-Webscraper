from bs4 import BeautifulSoup
import requests

def scrapeGame():
  pageToScrape = requests.get('https://j-archive.com/showgame.php?game_id=8792')
  soup = BeautifulSoup(pageToScrape.text, "html.parser")
  categories = soup.findAll('td', attrs={'class':'category_name'})
  category_comments = soup.findAll('td', attrs={'class':'category_comments'})
  # clue_value = soup.findAll('td', attrs={'class':'clue_value'})

  jeopardy_clues = []
  jeopardy_responses = []
  double_jeopardy_clues = []
  double_jeopardy_responses = []

  for x in range(1,6):
    for y in range(1,5):
      clue = soup.find('td', attrs={'id': f'clue_J_{x}_{y}'})
      response = soup.find('td', attrs={'id': f'clue_J_{x}_{y}_r'}).contents[0]
      if clue and response:
        jeopardy_clues.append(clue)
        jeopardy_responses.append(response)

      double_clue = soup.find('td', attrs={'id': f'clue_DJ_{x}_{y}'})
      double_response = soup.find('td', attrs={'id': f'clue_DJ_{x}_{y}_r'}).contents[0]
      if clue and response:
        double_jeopardy_clues.append(double_clue)
        double_jeopardy_responses.append(double_response)
  final_jeopardy_clue = soup.find('td', attrs={'id':'clue_FJ'})
  final_jeoupardy_response = soup.find('td', attrs={'id':'clue_FJ_r'}).contents[-1]

  for category, category_comment in zip(categories, category_comments):
    print(category.text + category_comment.text)
  for jeopardy_clue, jeopardy_response in zip(jeopardy_clues, jeopardy_responses):
    print(jeopardy_clue.text + " - " + jeopardy_response.text)
  for double_jeopardy_clue, double_jeopardy_response in zip(double_jeopardy_clues, double_jeopardy_responses):
    print(double_jeopardy_clue.text + " - " + double_jeopardy_response.text)
  print(final_jeopardy_clue.text + " - " + final_jeoupardy_response.text)

scrapeGame()