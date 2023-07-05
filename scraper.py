import bs4
import urllib.request


link = 'https://www.pathrise.com/guides/software-engine-resume-tips-with-sample-resume/'

class AppURLopener(urllib.request.FancyURLopener):
    version = "Mozilla/5.0"

opener = AppURLopener()
response = opener.open(link)

soup = bs4.BeautifulSoup(response)

print(soup.get_text())