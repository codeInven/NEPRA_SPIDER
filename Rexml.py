import xml.etree.ElementTree as ET
from xml.dom import minidom
import mysql.connector
from bs4 import BeautifulSoup
import urllib.request
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="nepra_search"
)
print(mydb)

# all items data  
mycursor = mydb.cursor()
# parse an xml file by name
mydoc = minidom.parse('sitemap.xml')
tree = ET.parse('sitemap.xml')
root = tree.getroot()

# all items data
print('Expertise Data:')
print(len(root[0]))
items = mydoc.getElementsByTagName('loc')
print(len(items))
#print(items[10104].firstChild.data)
#for elem in items:
#      print(elem.firstChild.data)

   #for subelem in elem:
#      print(elem.firstChild.text)

sql13= "insert into `site` (   `url`   ) VALUES (%s)"
sql_url= "insert into `site_url` (   `url`   ) VALUES (%s)"
sql_pdf= "insert into `site_pdf` (   `url`   ) VALUES (%s)"
sql_img= "insert into `site_image` (   `url`   ) VALUES (%s)"
def read_xml():
      try:

            for elem in items:
                  name=elem.firstChild.data
                  print(name)
                  mycursor.execute(sql13, (name,)) 
      except Exception as e:    
            print(e)
            mydb.close()

      mydb.commit()
      mydb.close()
def select_url():
      import os
      mycursor.execute("SELECT id,url FROM site")
      myresult = mycursor.fetchall()
      for urlid,x in myresult:
            filename, file_extension = os.path.splitext(x)
            #print(file_extension)
            
            try:
                  if (file_extension==".php"):
                         
                        mycursor.execute(sql_url, (x,)) 
                        print("-Php---pages")
                  elif(file_extension==".htm"):
                        print("Htm----Pages")
                        mycursor.execute(sql_url, (x,)) 
                  elif(file_extension==".html"):
                        print("hTML----Pages")
                        mycursor.execute(sql_url, (x,)) 
                  elif(file_extension==".pdf"):
                        print("-PDF----found")
                        mycursor.execute(sql_pdf, (x,)) 
                  elif(file_extension==".jpg"):
                        print("jpg----image")
                        mycursor.execute(sql_img, (x,)) 
                  elif(file_extension==".png"):
                        print("-png---image")
                        mycursor.execute(sql_img, (x,)) 
                  elif(file_extension==".tif"):
                        print("-tif---image")
                        mycursor.execute(sql_img, (x,)) 
                  
                  
                  #mycursor.execute(sql, (name, ))
                  
            except Exception as e:    
                  print(e)
      
      mydb.commit()
      mycursor.close()
sql4 = "insert into `html_content` (   `url_id` ,`title`,   `content`  ) VALUES (%s,%s,%s )"
def extract_html():
    mycursor.execute("SELECT id,url FROM site_url")
    myresult = mycursor.fetchall()
    for urlid,x in myresult:
        print(x)
        try:

            name=x
            print(name)
            #mycursor.execute(sql, (name, ))
            with urllib.request.urlopen(name) as url:
                s = url.read()
                soup = BeautifulSoup(s,'html.parser')
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
                print(soup.title.string)
                title=str(soup.title.string)
                print(len(str(text)))
                mycursor.execute(sql4, (urlid,title,text )) 
            mydb.commit()
        except Exception as e:    
                print(e)
    
    mydb.close()
extract_html()