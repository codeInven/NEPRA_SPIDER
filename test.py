
from bs4 import BeautifulSoup
import urllib.request

filepath = 'nepra_htm.txt'

 
url = "https://nepra.org.pk/careers.htm"
def rTitle(url,count):
    try:
        print("url out the url "+url)
        with urllib.request.urlopen(url) as url:
            s = url.read()
            soup = BeautifulSoup(s,'html.parser')
            # I'm guessing this would output the html source code ?
        
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
            
            
            print(soup.title.string)
            filename="nepra_{}.txt". format(count)
            print(filename)
            print(soup.title.string)
            with open(filename,"w+") as f:
                f.write(text)
             

            #title = soup.find("meta",  property="og:title")
    except:
        print("_+_=-=")
#f= open("nepra_htm.txt","w+")'''
def loop():
    with open(filepath) as fp:
        line = fp.readline()
        cnt = 1
        while line:
            rTitle(line.strip(),cnt)
            line = fp.readline()
            cnt += 1
'''with open(filepath) as fp:
    
    line = fp.readline()
    cnt = 1
    while line:
        print("Line {}: {}".format(cnt, line.strip()))
        
        #if line.strip().endswith(".htm"):
        #    f.write(line.strip()+"\n")
        rTitle(line.strip())
        line = fp.readline()
        cnt += 1'''
    #f.close()
rTitle(url,1)      

#import PyPDF2
# pdf file object
# you can find find the pdf file with complete code in below
#pdfFileObj = open('Hydel.pdf', 'rb')
# pdf reader object
#pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
# number of pages in pdf
#print(pdfReader.numPages)
# a page object
#pageObj = pdfReader.getPage(0)
# extracting text from page.
# this will print the text you can also save that into String
#print(pageObj.extractText())