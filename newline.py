import mysql.connector,time
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
 
 
sql = "INSERT INTO image_words (c_id,table_name,word) VALUES (%s,%s,%s)" 
 
 
def select_db(lid,jnumber):
    xsql="SELECT content FROM image_content where id={}". format(str(jnumber))
    print(xsql)
    mycursor.execute(xsql)
    myresult = mycursor.fetchall()
    for x in myresult:       
        try:
            for line in x:
                data=line.split(" ")
                for words in data:
                    rd=str(words)
                    #print('-{}-'. format(rd))
                    #print(len(rd))
                    lr=rd.split()
                    for g in lr:
                        print("={}=". format(g))
                            #time.sleep(1)
                        mycursor.execute(sql, (lid,'image_content',g ))
                mydb.commit()
                #print(line)        
        except :
            print('catch exception')
   

def kloop():
    for i in range(759):
        j=i+186
        xsql="SELECT id  FROM CONTENT where id={}". format(str(j))
        lid=0
        mycursor.execute(xsql)
        myresult = mycursor.fetchall()
        lid=myresult[0][0]
             

        select_db(lid,j) 
kloop()

          

            