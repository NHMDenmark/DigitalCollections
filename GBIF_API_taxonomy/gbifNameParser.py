#This code is meant to extract the ACCEPTED family name from a GBIF species search that will return multiple results in a json response

import requests
import pathlib
import time
import csv


def read_from_file(path, hasHeader=False):
    my_file = open(path, encoding='utf-8')
    content = my_file.read()
    content_list = content.split("\n")

    if hasHeader:
        content_list.pop(0)

    return content_list


def parse_name(input_list, kingdom, outputFile, header=False):
    #input_list : List of latin taxon names
    #taxon rank can be: kingdom, phylum, class, order, family, genus, species
    #outputFile: file to write

    if header: input_list.pop(0)
    with open(outputFile, 'a', newline='', encoding='utf-8') as o_file:
        #file object must be 'append' because the reference will be shared with the key error handler function repair_exception()
        header = 'scientificname;rank_;kingdom;phylum;class_;order_;family;genus;submitted_name\n'
        o_file.write(header)
        refined_initial = ""
        for name in input_list:
            api_call_template = "https://api.gbif.org/v1/species/match?kingdom={kingdom}&name={name}".format(kingdom=kingdom, name= name)
            print('api call: ', name, api_call_template)

            res = requests.get(api_call_template)
            rson = res.json()

            rank = 'rank'
            order = 'order'
            fam = 'family'
            class_ = 'class'
            kingdom = 'kingdom'
            phylum = 'phylum'
            sciname = 'scientificName'
            genus = 'genus'

            if len(rson) == 0:
                pass
            else:
                try:
                    rank = rson[rank]
                    sciname = rson[sciname]
                    phylum = rson[phylum]
                    class_ = rson['class']
                    order = rson[order]
                    fam = rson[fam]
                    genus = rson[genus]
                    mtype = rson["matchType"]

                    refined_initial = "{sciname};{rank_};{kingdom};{phylum};{class_};{order_};{family};{genus};{name}\n".format(sciname=sciname, rank_=rank,
                                                                                      kingdom = kingdom, phylum = phylum, class_=class_, order_=order,
                                                                                      family=fam, genus=genus, name=name)

                    print('NO error refined: ', refined_initial)

                except KeyError as ker:
                    print(rson)
                    print('keyerrr = ', ker)
                    rep = repair_exception(ker, rson, name, o_file)

                print('^-_-^', refined_initial)
                o_file.write(str(refined_initial))

def repair_exception(err, rson, submitted_name, file_ref, desired_keys=['scientificName', 'rank', 'phylum', 'class', 'order', 'family','genus', 'submitted_name']):
    #make err a variable name for position var in string refine
    myStr = err
    myVars = vars()
    myVars[myStr] = "py¤"
    #experimental for changing string into var name
    # newson = json.loads(rson)
    if rson['matchType'] == 'NONE':
        print('in MT NONE : ')
        response = 'NULL, NULL, NULL, NULL, NULL, NULL, NULL, {}'.format(submitted_name)
        print('the MT resp== ', response)
        return response

    remove_list = ['usageKey', 'canonicalName', 'status', 'confidence', 'matchType', 'kingdomKey', 'phylumKey',
                   'genusKey', 'synonym', 'classKey', 'orderKey']

    # print('remove list = ', remove_list)
    desired_terms = ['scientificName', 'rank', 'kingdom', 'phylum', 'class', 'order', 'family', 'genus', 'submitted_name']
    rson_keys = list(rson.keys())
    desired_dict = {elem:"NULL" for elem in desired_terms}
    #created a dict with default value NULL having the keys from
    desired_dict['kingdom'] = 'Plantae'

    existing_keys = list(set(desired_keys).intersection(rson_keys))
    print('EXISTING KEYS :', existing_keys)

    # desired.remove(err.args[0])
    for j in existing_keys:
        # print('jey:', j, 'des dict elem for j is:' , desired_dict[j], ' and dson value for j is; ', new[j])
        desired_dict[j] = rson[j]
    desired_dict['submitted_name'] = submitted_name
    print('final result== ', desired_dict)
    rson_keys = list(rson.keys())

    fieldnames = list(desired_dict.keys())
    # print('fieldnames --- : ', fieldnames)
    writer = csv.DictWriter(file_ref, fieldnames, delimiter=';')
    writer.writerow(desired_dict)


