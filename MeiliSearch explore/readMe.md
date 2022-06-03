# Test MeiliSearch solution to large a taxonomy in the App 'sputil'.

The purpose of this effort is to prototype a small search index solution to be used in conjunction with the SpUtil APP so that auto-suggest can be implemented. The auto-suggest feature requires very small latencies when users are typing in taxon names. Less than 20 milliseconds would be good.

## installation of MeiliSearch

I used Docker to install into my Linux laptop. Be mindful that you are downloading the latest version and change the version number accordingly.  

``` docker pull getmeili/meilisearch:v0.27.1```  

To run MeiliSearch:
```
docker run -it --rm \
-p 7700:7700 \
-v $(pwd)/meili_data:/meili_data \
getmeili/meilisearch:v0.27.1
```  


## Prepping the taxonomy file
Since MeiliSearch only supports json files for now, we need to turn the taxonomy csv file into that format.  
Be aware that Meilisearch requires an __ID field__ to be able to create the search index! If you wish to add a synthetic ID look here: https://stackoverflow.com/a/30530523
    
I used a Linux tool "JQ/csvtojson" to do the csv to json conversion :
```
apt-get install npm jq  
sudo apt-get install npm jq  
```  
Actual conversion step: 
```
csvtojson input.csv > output.json

```  


## Python specific for meilisearch_tryout.py  
Please install MeiliSearch from PIP : pip3 install meilisearch  
The json used in the code is here: https://alumni-my.sharepoint.com/personal/bxq762_ku_dk/_layouts/15/download.aspx?UniqueId=f89b67e8dc0f47eb8c6820a470360e14&e=7WeI2L  

There is a built in pause in the code that allows the index to be built. The json file is in this case 18MB and that takes a bit of time to turn into an index. 

