import requests
from bs4 import BeautifulSoup

programs_links = []
# able to capture all the pages of the URL #Selenium for Python can capture the javascript by simulaitn ga browser. Not used here.
for num in range(61):
	URL = 'http://healthmarketinnovations.org/programs/search?page='+ str(num)

	response = requests.get(URL)

	if response.status_code != 200:
		print 'Something went wrong'

	html = response.content
	soup = BeautifulSoup(html)

	base_url = 'http://healthmarketinnovations.org'
	anchor_title1 = soup.findAll('div',{'property' : 'dc:title'})

	for content in anchor_title1:
		anchor_title2 = content.findAll('a')
		for content in anchor_title2:
			link_suffix = content['href']
			full_link = base_url + link_suffix
			programs_links.append(full_link)

print programs_links
print len(programs_links)

#write the output of project_links in a json
import json
json.dump(programs_links, open("links.json","w")) 