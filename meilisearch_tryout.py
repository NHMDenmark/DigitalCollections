# -*- coding: utf-8 -*-
"""
  Created on Thu June 3, 10:21, 2022
  @author: Jan K. Legind, NHMD
  Copyright 2022 Natural History Museum of Denmark (NHMD)
  Licensed under the Apache License, Version 2.0 (the "License");
  you may not use this file except in compliance with the License.
  You may obtain a copy of the License at
  http://www.apache.org/licenses/LICENSE-2.0
  Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
  Plants of the World Online taxonomy https://hosted-datasets.gbif.org/datasets/wcvp.zip is used in this exploration. """

import meilisearch
import time
import json
from timeit import default_timer as timer
from datetime import timedelta


client = meilisearch.Client('http://127.0.0.1:7700')
#Local installation

def run_meiliSearch(inputFilePath, searchColumn, indexSearchTerm):
    '''Function takes an input json file and creates a MeiliSearch index. The indexSearchTerm is used to query the index.

    inputFilePath: the path to the json file
    searchColumn: the column (derived from a csv file header - see readMe) in the index that should be searched on.
    indexSearchTerm: the string that is the subject of the search.
    returns: the complete result of the search.'''

    json_file = open(inputFilePath)
    taxon = json.load(json_file)
    client.index(searchColumn).add_documents(taxon)
    time.sleep(8) #this break allows the index to complete building

    #Performance measure
    start = timer()
    result = client.index(searchColumn).search(indexSearchTerm, {'limit': 50})
    end = timer()
    performance = timedelta(seconds=(end - start))
    print('exe speed = ', performance)
    #end performance test
    return result


res = run_meiliSearch('jsonpowo.json', 'taxonname', 'Aalius compressa')
print('Number of hits = ', len(res['hits']))
#Total number of hits can be compared to a similar database query yielding a ground truth comparison with MeiliSearch result.
# Be aware that the MeiliSearch function has a hardcoded limit of 50!

topFive = res['hits'][:5]

for j in topFive:
    taxonName = j['taxonname']
    rank = j['rank_']
    print('taxon name = {} - rank : {}'.format(taxonName, rank))