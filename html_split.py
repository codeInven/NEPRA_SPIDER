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
 
 
#sql = "INSERT INTO html_split (url_id,text) VALUES (%s,%s)" 
 
#select *from (SELECT id,text FROM `html_split` where text like '%shahid mahmood%') as s

def select_db(dell):
    xsql="SELECT content FROM html_content where url_id={}". format(str(dell))
    lsql = "INSERT INTO html_split (url_id,text) VALUES (%s,%s)" 
    mycursor.execute(xsql)
    print(xsql)
    myresult = mycursor.fetchall()

    for x in myresult:       
        try:
            for line in x:
                data=line.split("\n")
                for words in data:
                    print((words))
                    mycursor.execute(lsql, ((dell),words))
                    #rd=str(words)
                    #print('-{}-'. format(rd))
                    #print(len(rd))
                    #lr=rd.split()
                    '''for g in lr:
                        print("={}=". format(g))
                            #time.sleep(1)
                        mycursor.execute(sql, (lid,'image_content',g ))'''
                #mydb.commit()
                
                mydb.commit()   
                     
        except :
            print('catch exception')
        
   
   

def kloop():
    for i in range(1,107):
        
        xsql="SELECT url_id  FROM html_CONTENT where id={}". format(str(i))
        mycursor.execute(xsql)
        myresult = mycursor.fetchall()
        lid=myresult[0][0] 
        print(lid)
        select_db(lid) 
        #mydb.close()
kloop()

          

            