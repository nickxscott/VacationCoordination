#flask imports
from flask import Flask,render_template,request,url_for,flash,jsonify,session,redirect, Markup, send_file
from flask_session import Session

#scheduling imports
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

#custom imports
from forms import *
from get import get_request

#python imports
import datetime
import holidays
import calendar
import random
import string
import pandas as pd

app = Flask(__name__, static_url_path='/static')
sk = ''.join(random.choices(string.ascii_uppercase +string.ascii_lowercase+string.digits, k=60))
app.secret_key = sk

#create schedule for get requests
#scheduler = BackgroundScheduler()
#trigger = CronTrigger(
#        year="*", month="*", day="*", hour="*", minute="*/10", second="0"
#    )
#scheduler.add_job(get_request, trigger=trigger)
#scheduler.start()


@app.route('/',methods=['GET','POST']) 
def home():
	form=holidayForm()
	year=datetime.date.today().year
	month=datetime.date.today().month

	try:
		df_holidays=pd.read_csv('holidays.csv')
	except:
		us_holidays = holidays.US(years = [year,year+1])
		d_weekdays={0:'Monday',1:'Tuesday',2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}
		
		df_holidays=pd.DataFrame(columns=['Date', 'Holiday', 'Joe', 'Taylor', 'Nick', 'Hayden', 'Jenny'])
		month_holidays=[]
		for d, h in us_holidays.items():
		    if d>=datetime.date.today():
		        l=len(df_holidays)
		        df_holidays.at[l,'date_raw']=d
		        df_holidays.at[l,'Date']=d_weekdays[d.weekday()]+', '+str(d)
		        df_holidays.at[l,'Holiday']=h
		df_holidays=df_holidays.sort_values(by='date_raw')
		df_holidays=df_holidays.fillna('Working')
	jenny=[]
	for index, row in df_holidays.iterrows():
		if row.Joe=='Off' and row.Taylor=='Off' and row.Hayden=='Off' and row.Nick=='Off':
			jenny.append('Off')
		else:
			jenny.append('Working')
	df_holidays.Jenny=jenny
	jenny_ct=len(df_holidays.loc[df_holidays.Jenny=='Off'])

	form.holiday.choices=[(row.Date, row.Date+' '+row.Holiday) for index, row in df_holidays.iterrows()]

	if request.method=='POST':
		user=form.user.data 
		hols=form.holiday.data
		avail=[]
		for index, row in df_holidays.iterrows():
			if row.Date in hols:
				avail.append('Off')
			else:
				avail.append('Working')
		df_holidays[user]=avail
		df_holidays.to_csv('holidays.csv',index=False)
		return redirect(url_for('home'))

	return render_template("home.html",
							df_holidays=df_holidays.loc[:,df_holidays.columns!='date_raw'],
							form=form,
							jenny_ct=jenny_ct)

@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"),404


@app.errorhandler(500)
def server_error(e):
	return render_template("500.html"),500


if __name__ == "__main__":
	app.run(host='localhost', port=5000,debug = True)

