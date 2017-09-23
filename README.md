# Flights Scrapper

This sorfware lets you find all the flights from Kayak from some given dates, and orders the by the price. To run it follow this tutorial:

First, make sure you are running from scratch using:

```
./clean.sh
```

Second, you have to create a file that contains one Kayak link per line. You should put this under the folder "links". For example the file links/links.txt would look like this

```
https://www.kayak.es/flights/ROM-MAD/2018-01-04-flexible/2018-01-05-flexible
https://www.kayak.es/flights/ROM-MAD/2018-01-04-flexible/2018-01-12-flexible
https://www.kayak.es/flights/ROM-MAD/2018-01-04-flexible/2018-01-19-flexible
https://www.kayak.es/flights/ROM-MAD/2018-01-04-flexible/2018-01-26-flexible
```

If instead of coping and pasting manually the links, you can use the tool "generate_links_kayak.py".
It generates two types of links. If you want a two ways trip. then the syntax is the following:

```
python generate_links_kayak.py -a <MM> -b <MM> -y <YYYY> -z <YYYY> -d <AIRPORT> -r <AIRPORT> -e <EXTENSION> -n <FILENAME>
```

This will find all the possible flight combinations between the two months. This means that there are 900 possible day combinations, but this software scans them all using only 25 links per doman

Each option is as follows

```
-a: month of the year of departure of the trip, ie, 01 is January, 09 is September, 12 is December
-b: month of the year of return from the trip, ie, 01 is January, 09 is September, 12 is December
-y: year of departure of the trip, ie, 2017
-z: year of return from the trip, ie, 2018
-d: code of the airport(s) of departure of the trip, ie, Madrid has the code MAD, Barcelona has the code BCN
    it is also possible to write several airports at the same time, ie, to find flights from
    Madrid (MAD) and Barcelona (BCN), write without spaces: MAD,BCN
-r: code of the airport(s) of destination of the trip. It is also possible to write several airports at the same time
    like with the option -d
-e: extension(s) of the Kayak domain to generate the links, ie, "es" will generate links from kayak.es or "co.uk" will
    generate links from kayak.co.uk
    If you want to generate from both domains at the same time, concatenate the extensions with a comma: es,co.uk
-n: path of the name of the file to write into (will append if it already exists), ie, links/links.txt
```

For example, if you want to go from Madrid or Barcelona in May of 2018 to Bangkok or Kuala Lumpur and return in June of 2018, and generate links from kayak.es and kayak.co.uk use the following command:

```
python generate_links_kayak.py -a 05 -b 06 -y 2018 -z 2018 -d MAD,BCN -r BKK,KUL -e es,co.uk -n links/links.txt
```

If instead you want a one way ticket, select -b 00 -z 00.

After the links are generated, use the python file "main.py" to scan and scrap the links:

```
python main.py <links-file> <path-to-phantomjs-binary>
```

For example:

```
python main.py links/links.txt phantomjs
```

This will download the HTML code of each link under the folder html. Then it will parse all the information of the flights like the price, airports, duration, dates, stops... and generate one csv file (separated by ;) per link under the folder csv.
Finaly to put them all together, you can run the following:

```
python analyze.py <folder>
```

For example
```
python analyze.py csv/
```

This will generate under that folder two files with the concatenated csv files and are ordered by price (less to more):

```
csv/results.csv
csv/results.html
```

Now is up to you what to do. This software can be used to monitor several trips and you could set up some kind of notification process to send you an email when you find a flight suitable for you. Nevertheless, keep in mind that Kayak does not like bots, and if you over use it, they will block you.

In summary, you have to run:

```
./clean.sh
python generate_links_kayak.py -a 05 -b 06 -y 2018 -z 2018 -d MAD,BCN -r BKK,KUL -e es -n links/links.txt
python main.py links/links.txt phantomjs
python analyze.py csv/
```