import operator
import datetime
import requests

from twilio.rest import Client

from bs4 import BeautifulSoup

def send_sms(msg):
	account_sid = "ACeff5916623198f15f795f595d1443f33"
	auth_token = "b507a5e49cbfba234e01e3258cdf1e45"
	client = Client(account_sid, auth_token)
	message = client.api.account.messages.create(to="+15083350510",from_="+19783476172",body=msg)

def average(ls):
	total = 0
	for elt in ls:
		total += float(elt)

	av = total/len(ls)
	return float("{0:.1f}".format(av))

def weather_report(url):
	page = requests.get(url)
	html = page.text

	soup = BeautifulSoup(html, "lxml")

	temps = soup.find_all('td', class_='temp')
	humidities = soup.find_all('td', class_='humidity')
	descriptions = soup.find_all('td', class_='hidden-cell-sm')
	di = {}

	for i, temp in enumerate(temps):
		if len(list(temp.children)) != 0:
			temps[i] = temp.get_text().encode('ascii', 'ignore')

	for i, humidity in enumerate(humidities):
		if len(list(humidity.children)) != 0:
			humidities[i] = humidity.get_text().encode('ascii', 'ignore')[:-1]

	for i, description in enumerate(descriptions):
		if len(list(description.children)) != 0:
			descriptions[i] = description.get_text().encode('ascii', 'ignore')
			if descriptions[i] not in di.keys():
				di[descriptions[i]] = 1
			else:
				di[descriptions[i]] += 1

	sorted_di = sorted(di.items(), key=operator.itemgetter(1))
	sorted_di.reverse()
	other =  ''

	most = sorted_di[0][1]
	for elt in sorted_di:
		if elt[1] >= most - 2:
			other += elt[0] + '/'
	other = other[:-1]

	ret = 'Average temperature: %s\n' % (str(average(temps)))
	ret += 'Average humidity: %s%%\n' % (str(average(humidities)))
	ret += 'Type of weather: %s\n' % (other)

	return ret


def main():
	now = datetime.datetime.now()
	msg = '\nReport for %d/%d: ' % (now.month, now.day)
	msg += '\n' + weather_report('https://weather.com/weather/hourbyhour/l/USMA0429:1:US')
	send_sms(msg)

if __name__=="__main__":
	main()

