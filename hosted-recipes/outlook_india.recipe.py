import json, re
from calibre.web.feeds.news import BasicNewsRecipe, classes

#TODO Learning 
_name = 'Outlook Magazine'
class outlook(BasicNewsRecipe):
    title = _name
    __author__ = 'unkn0wn'
    description = ''
    language = 'en_IN'
    use_embedded_content = False
    no_stylesheets = True
    remove_javascript = True
    compress_news_images = True
    compress_news_images_auto_size = 10
    scale_news_images = (800, 800)
    remove_attributes = ['height', 'width', 'style']
    ignore_duplicate_articles = {'url'}

    def parse_index(self):
        soup = self.index_to_soup('https://www.outlookindia.com/')
        a = soup.find('a', href=lambda x: x and x.startswith('/magazine/issue/'))
        url = a['href']
        self.log('Downloading issue:', url)
        soup = self.index_to_soup('https://www.outlookindia.com' + url)
        cover = soup.find(**classes('listingPage_lead_story'))
        self.cover_url = cover.find('img', attrs={'src': True})['src']
        ans = []

        for h3 in soup.findAll(['h3', 'h4'],
                               attrs={'class': 'tk-kepler-std-condensed-subhead'}):
            a = h3.find('a', href=lambda x: x)
            url = a['href']
            title = self.tag_to_string(a)
            desc = ''
            p = h3.find_next_sibling('p')
            if p:
                desc = self.tag_to_string(desc)
            self.log('\t\tFound article:', title)
            self.log('\t\t\t', url)
            ans.append({'title': title, 'url': url, 'description': desc})
        return [('Articles', ans)]

    def preprocess_raw_html(self, raw, *a):
        m = re.search('<!-- NewsArticle Schema -->.*?script.*?>', raw, flags=re.DOTALL)
        raw = raw[m.end():].lstrip()
        data = json.JSONDecoder().raw_decode(raw)[0]
        title = data['headline']
        body = data['articleBody']
        body = body.replace('\r\n', '<p>')
        author = ' and '.join(x['name'] for x in data['author'])
        image = desc = ''
        if data.get('image'):
            image = '<p><img src="{}">'.format(data['image']['url'])
        if data.get('description'):
            desc = '<h2>' + data['description'] + '</h2>'
        html = '<html><body><h1>' + title + '</h1>' + desc + '<h3>' + author + '</h3>' + image + '<p>' + body
        return html
