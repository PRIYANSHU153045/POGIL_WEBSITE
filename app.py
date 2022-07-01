
import pickle
import numpy as np
import requests
from flask import Flask, escape, flash, redirect, request, render_template, session, url_for, Markup
import os

from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
   return render_template('index.html')




@app.route('/news')
def news():
   from calendar import c
   headers={
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.74 Safari/537.36'
   }
   url='https://pogil.org/what-they-are-saying'
   r = requests.get(url, headers=headers)

   soup1 = BeautifulSoup(r.text, 'html.parser')
   
   news=soup1.find_all('div',class_='c-person c-person--small clearfix')
   
   newList=[]
   for item in news:
      List={
             'image':'https://pogil.org/'+item.find('img')['src'],
            'title': item.find('div',class_='c-person-formal-title').text,
            'info': item.find('div', {'class': 'c-person-title'}).text,
            'link':'https://pogil.org/'+ item.find('a',class_='c-person-more')['href'],
      }
      newList.append(List)
   return render_template('news.html',dict=newList)


# @app.route('/predict',methods=["POST","GET"])
# def predict():
#    if request.method=="POST":
#       print('hello')
       
#    else:
#       return render_template("predict.html")

#    return render_template('index.html')

   
# importing the pickle file 
file=open('Notebook/pogil2.pkl', 'rb')
pickled_model = pickle.load(file)

# file='Notebook/pogil1.pkl'

# if os.path.getsize(file) > 0:      
#     with open(file, "rb") as f:
#       unpickler = pickle.Unpickler(f)
#         # if file is not empty scores will be equal
#         # to the value unpickled
#       pickled_model = unpickler.load()

@app.route('/predict',methods=['GET','POST'])
def predict():
   if request.method=='POST':
      ssc=int(request.form['ssc'])
      if ssc >0:
         ssc=ssc
      else:
         ssc=0
      
      chemistry=int(request.form['chemistry'])
      if chemistry >0:
         chemistry=chemistry
      else:
         chemistry=0
      hsc=int(request.form['hsc'])
      if hsc >0:
         hsc=hsc
      else:
         hsc=0
      merit=int(request.form['merit'])
      if merit >0:
         merit=merit
      else:
         merit=0
      jee=int(request.form['jee'])
      if jee >0:
         jee=jee
      else:
         jee=0
      final1=int(request.form['final'])
      if final1 >0:
         final1=final1
      else:
         final1=0

      prediction = pickled_model.predict(
            np.array([[ssc, chemistry, hsc, merit, jee, final1]]))
      return render_template("predict.html", prediction_text="hey student this is your result: {}".format(prediction[0]))

   else:
      return render_template('predict.html') 


   # return render_template("predict.html") 


# file.flush()

@app.route('/powerbi')
def powerbi():
   return render_template('powerbi.html')


if __name__ == '__main__':
   app.run(debug = True)