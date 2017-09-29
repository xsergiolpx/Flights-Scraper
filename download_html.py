import random
from subprocess import call
from os import remove
from sys import platform


def download_html(link, html_name, phantomjs_bin = "./phantomjs", useragent = "phone", timeout_ms=5000, js_folder="javascripts/"):
    '''
    Uses phantomjs to download the HTML content executing all javascripts from
    a link.
    :param link: http link to download
    :param html_name: full filename to write into the HTML code
    :param phantomjs_bin: location of the binary
    :param useragent: string whichs says "phone" for a mobile user agent or anything else for desktop
    :return: Nothing
    '''

    # Create a random number for the names
    if useragent is "phone":
        user_agent = random.choice(list(open("useragents-phone.txt"))).replace("\n","")
    else:
        user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36"

    # Filenames
    sufix = "tmp" + str(random.randint(1, 10000000))
    js_name = js_folder + sufix + ".js"

    # Generate the phantomjs script with a template

    script = open('javascripts/dynamic-resources.js', 'r').read().replace("URL_HERE", link).replace("USERAGENT_HERE", user_agent).replace("HTML_SAVE_HERE",html_name)

    # Save it to a file
    print(script, file=open(js_name, "w+"))

    # Execute the script
    if "linux" in platform:
        t = "timeout"
    else:
        t = "gtimeout"
    call([t, "100", phantomjs_bin, js_name])

    # Delete the js script
    remove(js_name)
