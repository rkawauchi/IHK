import requests
from bs4 import BeautifulSoup
from datetime import datetime

url = 'http://healthmarketinnovations.org/program/sana-mobile'

def fix_date(string):
	return datetime.strptime(string, '%B %d, %Y').strftime('%Y-%d-%m')

def parse_page(url):
	data_dict = {}
	response = requests.get(url)
	if response.status_code != 200:
		print 'Something went wrong'
	html = response.content
	soup = BeautifulSoup(html)

	#title
	span_tags = soup.findAll('h1', {'class': 'page-title'})
	title = span_tags[0].text.strip()
	data_dict['title'] = title

	#year
	span_tags = soup.findAll('div', {'class': 'group-header'})
	span_tags1 = span_tags[0].findAll('span')
	year = span_tags1[1].text.strip()
	data_dict['year'] = year

	#profit status
	span_tags = soup.findAll('p', {'class': 'profit-status'})
	if span_tags != []:
		profit_status = span_tags[0].text.strip()
	else:
		profit_status = 'Unknown'
	data_dict['profit_status'] = profit_status

	#categories
	span_tags = soup.findAll('div', {'class': 'group-header'})
	span_tags1 = span_tags[0].findAll('span', {'class': 'lineage-item lineage-item-level-1'})
	categories = []
	for i in span_tags1:
		a_tag = i.findAll('a')
		category = a_tag[0].text.strip()
		categories.append(category)
	data_dict['categories'] = categories

	#health focus
	span_tags = soup.findAll('div', {'class': 'field field--field-profile-health-focus field-label--inline'})
	span_tags1 = span_tags[0].findAll('span', {'class': 'lineage-item lineage-item-level-0'})
	health_focus = []
	for i in span_tags1:
		focus = i.a.text.strip()
		health_focus.append(focus)
	data_dict['health_focus'] = health_focus

	#locations
	#country + regions
	span_tags = soup.findAll('ul', {'class': 'term'})
	country = span_tags[0].li.a.text.strip() #If multiple countries, doesn't handle
	regions = []
	for i in span_tags[0].li.ul.findAll('li'):
		span_tags1 = i.findAll('a')
		regions.append(span_tags1[0].text.strip())
	data_dict['country'] = country
	data_dict['regions'] = regions

	#summary
	stringsA = []
	span_tags = soup.findAll('div', {'class': 'group-middle'})
	for string in span_tags[0].strings:
    	stringsA.append(string)
    print stringsA
	#summary = span_tags[0].string.strip()
	#data_dict['summary'] = summary

	print data_dict

	"""
	

	#categories
	span_tags = soup.findAll('div', {'class': 'field field--field-profile-core-activities field-label--inline'})
	span_tags2 = span_tags[0].findAll('span', {'class': 'lineage-item lineage-item-level-1'})
	for i in span_tags2:
		category = i.findAll('a')


	location = span_tags[0].text.strip()
	data_dict['location'] = location

	#amount raised
	span_tags = soup.findAll('span', {'class': 'currency currency-xlarge'})
	first_span = span_tags[0]
	dollar_string = span_tags[0].findAll('span')[0].text.strip()

	#conversion of the amount
	money = ""
	for character in dollar_string:
		if character.isdigit():
			money = money + character
	data_dict['amount_raised'] = category

	#campaign duration
	span_tags = soup.findAll('p', {'class': 'funding-info'})
	paragraph = span_tags[0]
	print paragraph

	#start and end
	#we could use the landmark 'Funding duration:' but we will use regular expression here
	import re #importing regular expression
	dates = re.findall(r'[A-Z][a-z]+ [0-9]{2}, [0-9]{4}',paragraph.text) #r'regularexpression', where {repeated X times}	
	start_date = dates[0]
	end_date = dates[1]
	start_date = fix_date(start_date)
	end_date = fix_date(end_date)
	print start_date, end_date

	data_dict['start_date'] = start_date
	data_dict['end_date'] = end_date
	"""




## Putting this in a database

# import json
# links = jsn.load(open('links.json'))
# 	output = parse_page(link)
# 	line = '{url}\t{category}\t{start_date}\t{end_date}\t{location}\t{amount_raised}'.format(**output) 
# 	# keys in a dictionnary where we can replace the fields. output is a dictionnary. 
# 	#Takes the url key in the data dictionnary and replace it with the output value
# 	print line

parse_page(url)
