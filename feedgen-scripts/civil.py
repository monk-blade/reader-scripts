import requests # pip install requests
from datetime import datetime, timezone
from bs4 import BeautifulSoup as bs # pip
from feedgen.feed import FeedGenerator
from dateutil import parser
import pytz
fg = FeedGenerator()
fg.id('http://lernfunk.de/media/654321')
fg.title('CivilsDaily Feeds')
fg.author({'name': 'CD Team', 'email': 'john@example.de'})
fg.link(href='https://civilsdaily.com', rel='alternate')
fg.logo('http://ex.com/logo.jpg')
fg.subtitle('This is generated feed from main website.')
fg.link(href='http://larskiesow.de/test.atom', rel='self')
fg.language('en')

p = requests.get("https://www.civilsdaily.com/news/")
soup2 = bs(p.content,'lxml')

for article in soup2.find_all('article'):
    entry = fg.add_entry()
    #get title of text
    title_text = article.find('h1').get_text()
    entry.title(title_text)
    #get url link of post
    link_text = article.find("span", {"class": "meta-text"})
    link_url = link_text.find('a')['href']
    date_text = link_text.get_text()
    # converting date string to datetime object
    dt = parser.parse(date_text)
    final_date = dt.replace(tzinfo=pytz.timezone('Asia/Kolkata'))
    entry.pubDate(final_date)
    #extracting content as html
    post_text = article.find("div", {"class": "post-inner"})
    content_text = str(post_text).strip()
    entry.id(link_url)
    entry.link(href=link_url, rel='alternate')
    entry.content(content_text,type="CDATA")

#atomfeed = fg.atom_str(pretty=True)
fg.rss_file('rss.xml')

# fg = FeedGenerator()
# fg.id('http://lernfunk.de/media/654321')
# fg.title('Some Testfeed')
# fg.author( {'name':'John Doe','email':'john@example.de'} )
# fg.link( href='http://example.com', rel='alternate' )
# fg.logo('http://ex.com/logo.jpg')
# fg.subtitle('This is a cool feed!')
# fg.link( href='http://larskiesow.de/test.atom', rel='self' )
# fg.language('en')

# Load the webpage content
# r = requests.get("https://www.drishtiias.com/hindi/current-affairs-news-analysis-editorials")
# soup = bs(r.content)

# for link in soup.select(".box-toggle:nth-child(2) .box-slide , .box-hide a"):
#   regexp = re.compile('.*news-editorials.*')
#   #spacn = link.find_all("href", string=re.compile("August"))
#   #print(spacn)
#   editorial_url = regexp.findall(link['href'])
#   if(editorial_url):
#     print(editorial_url)