import requests
import html2text
import urllib
url="http://www.nepra.org.pk"
r = requests.get(url)
h = requests.head(url, allow_redirects=True)
header = h.headers
content_type = header.get('content-type')
content_length = header.get('content-length', None)
#text_maker = html2text.html2text()
with urllib.request.urlopen(url) as response:
   html = response.read()
   #print(html)
   #ext = text_maker.handle(html)
   #print(text)


 
 # Ignore converting links from HTML
h = html2text.HTML2Text()
print(h.handle("<p>Hello, <a href='https://www.google.com/earth/'>world</a>!"))