import feedparser

url =  'http://alerts.weather.gov/cap/us.php?x=0'   
p = feedparser.parse(url)
print('status: %s' % (p.status))

print(p.entries)

#['summary_detail', 'published_parsed', 'links', 'title', 'feedburner_origlink', 'tags', 'summary', 'guidislink', 'title_detail', 'link', 'published', 'id']

for entry in p.entries:

    print(entry['published_parsed'])
    #print(entry['summary_detail']['value'])
    #print(entry['links'])
