import requests

def get_request():
	x = requests.get('https://vacationcoordination.onrender.com')
	print(x.status_code)