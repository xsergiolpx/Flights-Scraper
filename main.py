from download_html import download_html
from parse_html import parse_kayak_mobile
from export_csv import export_list_dict_csv
import random
from time import gmtime, strftime
from export_csv import import_list
import sys
from time import sleep

#phantomjs_path = "bin/phantomjs-2.1.1-macosx/bin/phantomjs"

def wait(time=60):
    '''
    Sleeps a random time in seconds from time/2 to time + time/2
    :param time: int, in seconds
    :return: nothing
    '''
    s = random.randrange(int(time/2), int(time + time/2))
    sleep(s)

if len(sys.argv) is not 4:
    print("Syntax error, use: \n   python main.py <links-file> <path-to-phantomjs-binary>"
          "\n ie: \n python main.py links/links.txt phantomjs")
else:
    links_file = sys.argv[1]
    phantomjs_path = sys.argv[2]
    sleeping_time = int(sys.argv[3])

links = import_list(links_file)
random.shuffle(links)
links = set(links)

# Variables for the loop
max_links = len(links)
links_repeat = set()
timeout = 25000
counter = 0

# Pop links until finish
while len(links) > 0:
    link = links.pop()
    print("["+ str((round((max_links-len(links))/max_links*100))) + "%] Downloading " + str(max_links-len(links))+ "/" + str(max_links) + " links   ", link)
    # Generate a name to download this data
    sufix = strftime("%d-%m-%Y-%Hh-%Mm-%Ss", gmtime()) + "-tmp" + str(random.randint(1, 10000000))

    # Where to create the file
    html_folder = "html/"
    html_name = html_folder + sufix + ".html"
    csv_folder = "csv/"
    csv_name = csv_folder + sufix + ".csv"

    # Get the data
    download_html(link=link, html_name=html_name, phantomjs_bin=phantomjs_path, useragent = "phone", timeout_ms=timeout)
    data = parse_kayak_mobile(filename=html_name, link=link)

    # Check that there is data parsed
    if len(data) > 0:
        print("Link OK... \n\n")
        export_list_dict_csv(list_of_dicts=data, filename=csv_name)
    else:
        print("Link failed! Try one more time later... \n\n")
        # Add to get them again
        links_repeat.add(link)
    # Count the times of loops done
    counter = counter + 1

    # Add the bad links to try again
    if counter is max_links:
        links = links.union(links_repeat)
        timeout = timeout * 3

    sleep(sleeping_time)

