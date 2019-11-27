from PIL import Image
import sys,time
import pyocr
import pyocr.builders

import mysql.connector
import urllib.request
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="nepra_search"
)

print(mydb)
mycursor = mydb.cursor()
  
def Download_Progress(block_num, block_size, total_size):
    downloaded = block_num * block_size
    progress = int((downloaded/total_size)*100)
    print ("Download Progress",str(progress),"%")
    
sql = "INSERT INTO image_content (imurl_id,content) VALUES (%s,%s)" 
pyocr.tesseract.TESSERACT_CMD = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
# The tools are returned in the recommended order of usage
tool = tools[0]
print("Will use tool '%s'" % (tool.get_name()))
# Ex: Will use tool 'libtesseract'

langs = tool.get_available_languages()
print("Available languages: %s" % ", ".join(langs))
lang = langs[4]
print("Will use lang '%s'" % (lang))
# Ex: Will use lang 'fra'
# Note that languages are NOT sorted in any way. Please refer
# to the system locale settings for the default language
# to use.
'''txt = tool.image_to_string(
    Image.open('news.jpg'),
    lang=lang,
    builder=pyocr.builders.TextBuilder()
)
print(txt)'''


 
def select_db():
    mycursor.execute("SELECT * FROM `site_image` WHERE image not like '%.tif'")
    myresult = mycursor.fetchall()
    
    for pid,x in myresult:
       
        try:
            name=x
            print("{},{}". format(pid,x))
        #mycursor.execute(sql, (name, ))
            #test(pid,name)
        except :
            print('catch exception')
    #mydb.commit()
 
#pid,name
def test():
    filename='test.jpg'
    print('...Starting..........')
    #urllib.request.urlretrieve(name, filename,reporthook=Download_Progress)
    #time.sleep(20)
    txt = tool.image_to_string(
    Image.open(filename),
    lang=lang,
    builder=pyocr.builders.TextBuilder())
    lines = (line.strip() for line in txt.splitlines())
    #print(lines) 
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    print(text)
    #mycursor.execute(sql, (pid,text, )) 
    print('Finish')
   # mydb.commit()
test()