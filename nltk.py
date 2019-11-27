


import urllib.request
from bs4 import BeautifulSoup
from nltk import FreqDist

response =  urllib.request.urlopen('https://en.wikipedia.org/wiki/SpaceX')
html = response.read()
print(html)

soup = BeautifulSoup(html,'html.parser')
# kill all script and style elements
for script in soup(["script", "style"]):
    script.extract()    # rip it out

# get text
text = soup.get_text()

# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text.splitlines())
print(lines) 
# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
text = '\n'.join(chunk for chunk in chunks if chunk)
 
print(text)
tokens = [t for t in text.split()]
print(tokens)
from stop_words import get_stop_words

stop_words = get_stop_words('en')
 
clean_tokens = tokens[:]
for token in tokens:
    if token in get_stop_words('en'):
        
        clean_tokens.remove(token)

freq =FreqDist(clean_tokens)
for key,val in freq.items():
    print(str(key) + ':' + str(val))
freq.plot(20, cumulative=False)
