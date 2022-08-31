'''Simple version of gbifNameParser.py'''
import requests
import pathlib
import time
import csv


def read_from_file(path):
    my_file = open(path, encoding='utf-8')
    content = my_file.read()
    content_list = content.split("\n")

    sub = content_list[:15]

    return content_list

has_header = False

def parse_name(input_list, kingdom, outputFile):
    #input_list : List of latin taxon names
    #taxon rank can be: kingdom, phylum, class, order, family, genus, species
    #outputFile: file to write

    # input_list.pop(0)
    with open(outputFile, 'a', newline='', encoding='utf-8') as o_file:
        #file object must be 'append' because the reference will be shared with the key error handler function repair_exception()
        header = 'scientificname;kingdom;phylum;class_;order_;family;genus;submitted_name\n'
        o_file.write(header)
        refined_initial = ""
        for name in input_list:
            #https://api.gbif.org/v1/species/match?kingdom=Plantae&name=Abies%20alba
            api_call_template = "https://api.gbif.org/v1/species/match?kingdom={kingdom}&name={name}".format(kingdom=kingdom, name=name)

            #CLEAN OUT BOM FROM INPUT FILE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            print('api call: ', name, api_call_template)

            res = requests.get(api_call_template)
            rson = res.json()

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
                    sciname = rson[sciname]
                    phylum = rson[phylum]
                    class_ = rson['class']
                    order = rson[order]
                    family = rson['family']
                    # genus = rson[genus]
                    kingdom = rson['kingdom']
                    mtype = rson["matchType"]
                    # print(rank, class_, order, fam, sciname, 'submitted : ', name)
                    # global refined_initial
                    refined_base = {'sciname':'','kingdom':'Plantae','phylum':'','class':'','order': '', 'family':'', 'submitted':''}
                    refined_end = {'sciname':sciname,'kingdom':kingdom,'phylum':phylum,'class':class_,'order':order, 'family':family, 'submitted':name}
                    # refined_initial = "{sciname};Plantae;{phylum};{class_};{name}\n".format(sciname=sciname, rank_=rank,
                    #                                                                   phylum = phylum, class_=class_,
                    #                                                                   family=fam, genus=genus, name=name)
                    # refined = "{sciname};{rank_};{class_};{order_};{family}\n".format(sciname = name, rank_ = rank, class_=class_, order_=order, family=fam)
                    print('NO error refined: ', refined_end)
                    # break
                except KeyError as k:
                    print(rson)
                    print('keyerrr = ', k)
                    print('ref_end: ', rson)
                    print('inside kerror= ', k.args[0])
                    refined_end[k.args[0]] = 'NULL'
                    print('refined:: ', refined_end)


                    # refbase= refined_base.format(k)

                    # if name:
                        # print('THE NAME IS ===', name)
                    # rep = repair_exception(k, rson, name, o_file)
                    # print(rep)
                    # rep = ';'.join(rep)
                    # refined_initial = rep
                    continue

                print('^--^', refined_end)

                w = csv.DictWriter(o_file, refined_end.keys(), delimiter=';')
                if has_header:
                    w.writeheader()
                w.writerow(refined_end)
                # o_file.write(str(refined_end))

lst = read_from_file('C:/Users/bxq762/Documents/exports/herbvascutil.txt')
rr = parse_name(lst, 'Plantae', 'C:/Users/bxq762/Documents/taxonomy/herbhigherutil.txt')