import requests
from bs4 import BeautifulSoup


class Scrapper():
  def scrap_page(self, url: str):
    is_wikipedia_link = self.validate_url(url)
    
    if(not is_wikipedia_link): 
      raise ValueError("URL must be from pt.wikipedia.org/wiki")
    
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(response.content, 'html.parser')
  
    paragraphs = soup.find_all('p')
    text = ' '.join([p.get_text() for p in paragraphs])
    
    return text
  
  def validate_url(self, url:str): 
    return url.startswith("https://pt.wikipedia.org/wiki/")