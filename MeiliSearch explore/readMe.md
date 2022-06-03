# Test MeiliSearch solution to large a taxonomy in the App 'sputil'.

The purpose of this effort is to prototype a small search index solution to be used in conjunction with the SpUtil APP so that auto-suggest can be implemented. The auto-suggest feature requires very small latencies when users are typing in taxon names. Less than 20 milliseconds would be good.

## installation of MeiliSearch

I used Docker to install into my Linux laptop.  

``` docker pull getmeili/meilisearch:v0.27.1```  

To run MeiliSearch:
```
docker run -it --rm \
-p 7700:7700 \
-v $(pwd)/meili_data:/meili_data \
getmeili/meilisearch:v0.27.1
```  

## Python specific  
Please install MeiliSearch from PIP : pip3 install meilisearch  

## Prepping the taxonomy file
Since MeiliSearch only supports json files for now, we need to turn the taxonomy csv file into that format.  
Be aware that Meilisearch requires an __ID field__ to be able to create the search index! 
    
```
awk -F',' -v OFS=',' 'NR == 1 {print "ID", $0; next} {print (NR-1), $0}'  
wpow_199k.csv  > output.csv
```
I used a Linux tool "JQ/csvtojson" to do the csv to json conversion :
```
apt-get install npm jq  
sudo apt-get install npm jq

```  

