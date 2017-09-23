import random
from subprocess import call
from os import remove
from sys import platform

def download_html(link, html_name, phantomjs_bin = "./phantomjs", useragent = "iphone", timeout_ms=5000):
    '''
    Uses phantomjs to download the HTML content executing all javascripts from
    a link.
    :param link: http link to download
    :param html_name: full filename to write into the HTML code
    :param phantomjs_bin: location of the binary
    :param useragent: string whichs says "iphone" for a mobile user agent or anything else for desktop
    :return: Nothing
    '''

    # Create a random number for the names
    if useragent is "iphone":
        user_agent = "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2_1 like Mac OS X) AppleWebKit/602.4.6 (KHTML, like Gecko) Version/10.0 Mobile/14D27 Safari/602.1"
    else:
        user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36"

    # Folders
    js_folder = "javascripts/"

    # Filenames
    sufix = "tmp" + str(random.randint(1, 10000000))
    js_name = js_folder + sufix + ".js"

    # Generate the phantomjs script
    script = "var page = new WebPage()\n " \
             "var fs = require('fs'); " \
             "page.settings.userAgent = '" + user_agent + "';" \
             "page.settings.resourceTimeout = "+ str(timeout_ms) +"; var settings = {encoding: 'utf8',};" \
             "page.onLoadFinished = function() {" \
             "console.log('Page load finished!');" \
             "fs.write('" + html_name + "', page.content, 'w');" \
             "phantom.exit();};" \
             "page.open('" +  link + "', function() {" \
             "page.evaluate(function() {});});"

    # Save it to a file
    print(script, file=open(js_name, "w+"))

    # Execute the script
    if "linux" in platform:
        t = "timeout"
    else:
        t = "gtimeout"
    call([t, "60", phantomjs_bin, js_name])

    # Delete the js script
    remove(js_name)