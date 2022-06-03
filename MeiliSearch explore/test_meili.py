import meilisearch
import json, csv, time
from timeit import default_timer as timer
from datetime import timedelta


client = meilisearch.Client('http://127.0.01:7700')
# client.delete_index('movies')
# json_file = open('wpow_200k.csv')
# taxon = 'wpow_199k.csv'
csv_file = 'wpow_199k.csv'
json_file = 'wpow.json'
data = {}
with open(csv_file) as csvfile:
    csvReader = csv.DictReader(csvfile)
    for row in csvReader:
        # print(row)
        # break
        id = row['taxonname']
        data[id] = row

with open(json_file, 'w') as jfile:
    jfile.write(json.dumps(data, indent=4))


json_file = open('wpow.json')
taxonomy = json.load(json_file)
client.index('taxonomy').add_documents(taxonomy)


#
st = client.index('taxonomy').get_stats()
while st['isIndexing']:
    print(st['isIndexing'])
    print('stats --- ', st)
    st = client.index('taxonomy').get_stats()
    time.sleep(10)

time.sleep(60)
print('STATS - - ', st)
print('CLIENT ', client.get_index('taxonomy'))
print(client.index('taxonomy').get_task(61))

ranking = client.index('taxonomy').get_ranking_rules()
print("RANKING RULEZ = ", ranking)
print(client.index('taxonomy').update_ranking_rules(
    ['words', 'typo', 'proximity', 'attribute', 'sort', 'exactness']
))
print("new RANKING RULEZ = ", ranking)
start = timer()
time.sleep(120)
search_res = client.index('taxonomy').search('Abasicarpon')
print(search_res)
# end = timer()
#
# td = end - start
# performance = timedelta(seconds=td)
# print('seconds == ', performance.total_seconds() )