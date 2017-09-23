import csv

def export_list_dict_csv(list_of_dicts, filename):
    keys = list_of_dicts[0].keys()
    with open(filename, 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys, delimiter=";")
        dict_writer.writeheader()
        dict_writer.writerows(list_of_dicts)

def export_list_csv(thelist, filename):
    thefile = open(filename, 'a+')
    for item in thelist:
        thefile.write("%s\n" % item)

def import_list(filename):
    return [line.rstrip('\n') for line in open(filename)]
