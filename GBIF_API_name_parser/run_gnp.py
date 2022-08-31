import gbifNameParser


lst = gbifNameParser.read_from_file('C:/Users/bxq762/Documents/exports/family_gimme_HT.txt', hasHeader=True)
rr = gbifNameParser.parse_name(lst, 'Plantae', 'C:/Users/bxq762/Documents/taxonomy/family_clean.tsv')
