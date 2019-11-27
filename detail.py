import urllib.request
from urllib.parse import urlsplit, urlunsplit, urljoin, urlparse
import re



	 

	 
url="http://www.nepra.org.pk"

found_links=[]
found_detail=[] 
  
try:
    response = urllib.request.urlopen(url)
    page = str(response.read())

    pattern = '<a [^>]*href=[\'|"](.*?)[\'"].*?>'
    found_links = re.findall(pattern, page)
    print(found_links)
     
    for de in found_links:
        pirnt(de)
    #print(found_links)
    links = []
    
        
    
except:
    print("----")

 

	 