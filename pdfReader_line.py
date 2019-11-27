from PyPDF4 import   PdfFileReader
 
import numpy as np
import urllib.request
import mysql.connector
from io import StringIO
from spellchecker import SpellChecker
spell = SpellChecker()
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="root",
  database="RPM"
)

print(mydb)
sql = "INSERT INTO pdf_content (Pdf_id,page,Content) VALUES (%s,%s,%s)" 
# all items data  
mycursor = mydb.cursor()
pdf_id=0
def select_db():
    mycursor.execute("SELECT id,url FROM site_pdf ")
    myresult = mycursor.fetchall()
    print('...Starting..........')
    for pid,x in myresult:
       
        try:
             
            print("{},{}". format(pid,x))
        #mycursor.execute(sql, (name, ))
            #test(pid,x)
        except Exception as e:
            print(e)
    #mydb.commit()
 
#pid,name
def test():
    sql = "INSERT INTO letters (words) VALUES (%s)" 
    filename='dan_brown.pdf'
    print('...Starting..........')
    #urllib.request.urlretrieve(name, filename)
    pdf = PdfFileReader(open(filename, "rb"))
    info = pdf.getDocumentInfo()
    print(info)
    info = pdf.getNumPages()
    print("Numbers of pages {} ". format(info))
    for i in range(info):

        x=pdf.getPage(i)
        text=x.extractText()
       
        lines = (line.strip() for line in text.splitlines())
       
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        #print(text)
        data=text.split("\n")
        for line in data:
            #print((words))
            
            words=line.split(" ")
            for letter in words:
                print("--{}--". format(letter))
                mycursor.execute(sql, (letter, ))

            #rd=str(words)
            #print('-{}-'. format(rd))
            #print(len(rd))
            #lr=rd.split()
            # data=text.split("\n")
        #print("--{}--". format(text) )
        #mycursor.execute(sql, (pid,i,text, )) 
    print('Finish')
    mydb.commit()


def sepllch():
    mycursor.execute("SELECT words FROM dan ")
    myresult = mycursor.fetchall()
    print('...Starting..........')
    for pid in myresult:
       
        try:
            print((spell.candidates(pid[0])))
            print("{}--". format(pid[0]))
        #mycursor.execute(sql, (name, ))
            #test(pid,x)
        except Exception as e:
            print(e)


sepllch()