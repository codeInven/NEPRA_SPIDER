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
val="kill" 
 
sql1 = "INSERT INTO site_url (url_id,content) VALUES (%s,%s)" 
sql2 = "insert into `bk_nepra_words` ( `id`,`c_id`,`table_name`,`word`) VALUES (%s,%s,%s,%s)"
sql3 = "insert into `content` (`id`,`Pdf_id`,`page`,`content``) VALUES (%s,%s,%s,%s)"
sql4 = "insert into `html_content` (   `url_id` ,`title`,   `content`  ) VALUES (%s,%s,%s )"
sql5 = "insert into `iamge_words` (  `id` ,   `c_id`,   `table_name`,   `word` )  VALUES (%s,%s,%s,%s)"
sql6 = "insert into `image_content` (  `id`  ,   `imurl_id` ,  `content` )  VALUES (%s,%s,%s)"
sql7 = "insert into `image_words` ( `id` ,   `c_id` ,   `table_name`,   `word`  ) VALUES (%s,%s,%s,%s)"
sql8 = "insert into `nepra_words` (  `id`  ,   `c_id` ,   `table_name` ,   `word`  ) VALUES (%s,%s,%s,%s)"
sql9 = "insert into `pdf_content_words` (  `id` ,   `c_id` ,   `table_name` ,   `word` ) VALUES (%s,%s,%s,%s)"
sql10= "insert into `site_excle` (  `id`  ,   `link`  )  VALUES (%s,%s)"
sql11= "insert into `site_image` (     `url`  )  VALUE     (%s )"
sql12= "insert into `site_pdf` (     `url`  ) VALUE (%s)"
sql13= "insert into `site_url` (   `url`   ) VALUES (%s)"
 
 
def select_db():
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


def file_re():
    #@nepra.org.pk

    with open('h:/sitemap_26_aug.xml') as fp:
        line = fp.readline()
        while line:
            
            if (line[-4:-1]=="png"):
                print(line[-4:-1])
                try:
                    name=line.strip()
                    name=str(name)
                    print(name)
                    
                    #mycursor.execute(sql, (name, ))
                    
                    
                    '''with urllib.request.urlopen(name) as url:
                        s = url.read()
                        soup = BeautifulSoup(s,'html.parser')
                        # kill all script and style elements
                        for script in soup(["script", "style"]):
                            script.extract()    # rip it out
'''


                        # get text
                        #text = soup.get_text()
                        
                        # break into lines and remove leading and trailing space on each
                        #lines = (line.strip() for line in text.splitlines())
                        #print(lines) 
                        # break multi-headlines into a line each
                        #chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                        # drop blank lines
                        #text = '\n'.join(chunk for chunk in chunks if chunk)
                        #print(line.strip())
                        #print(soup.title.string)                        val= str(soup.title.string) 

 

                    mycursor.execute(sql11, (name,)) 
                except Exception as e:    
                    print(e)
            line = fp.readline()
        mydb.commit()
        mydb.close()
    print(mycursor.rowcount, "record inserted.")

select_db()