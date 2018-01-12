import datetime
import sys, getopt
from export_csv import export_list_csv
import calendar

def diff_days(a,b):
    '''
    Returns the diference of days
    :param a: like "2017-12-30"
    :param b: same
    :return: difference of days as int
    '''
    a = datetime.datetime.strptime(a, "%Y-%m-%d")
    b = datetime.datetime.strptime(b, "%Y-%m-%d")
    return int((b - a).days)

def clean_dates(all_dates):
    return all_dates

def gen_dates_same_month(day1, day2, month, year):
    '''
    :param day1: day of the week, like "monday"
    :param day2: day of the week, like "tuesday"
    :param month: month to generate dates: ie "03" is march
    :param year:
    :return: something like [['2017-04-04', '2017-04-05'], ['2017-04-04', '2017-04-12']]
    '''
    month=int(month)
    year=int(year)
    c = calendar.Calendar(firstweekday=calendar.MONDAY)
    vec_days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    if vec_days.index(day1) - vec_days.index(day2) >= 0:
        dif = - vec_days.index(day1) + vec_days.index(day2) + 7
    else:
        dif = vec_days.index(day2) - vec_days.index(day1)
    print(dif)
    monthcal = c.monthdatescalendar(year, month)
    d = [[datetime.date(day.year, day.month, day.day).strftime("%Y-%m-%d"),
          (datetime.date(day.year, day.month, day.day) + datetime.timedelta(days=dif)).strftime("%Y-%m-%d")]
         for week in monthcal for day in week if day.weekday() == vec_days.index(day1) and day.month == month]
    return d


def gen_dates_no_return(day1, month, year):
    month = int(month)
    year = int(year)
    c = calendar.Calendar(firstweekday=calendar.MONDAY)
    vec_days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    monthcal = c.monthdatescalendar(year, month)
    d = [[datetime.date(day.year, day.month, day.day).strftime("%Y-%m-%d"), "no-return"]
         for week in monthcal for day in week if day.weekday() == vec_days.index(day1) and day.month == month]
    return d

def gen_dates(day1,day2,month_departure, year_departure):
    '''
    generates the list of lists for departure and return dates
    :param month_departure: i.e "03" for march
    :param month_return: i.e "06" for june
    they have to be str of two characters
    :return: list of lists with possible departure dates and return dates in each element
    i.e [['2017-03-04', '2017-04-04'], ['2017-04-04', '2017-05-11']]
    '''
    if day2 == "00":
        return gen_dates_no_return(day1, month_departure, year_departure)
    else:
        return gen_dates_same_month(day1, day2, month_departure, year_departure)


def gen_links(dates, airport_departure, airport_arrival, extensions = ["es"]):
    '''
    creates the links to scrape in the form:
    https://www.kayak.es/flights/FCO-BKK,KUL/2017-04-11-flexible/2017-07-02-flexible
    :param dates: list of lists of two elements with departure date and return date in the following form:
    [["2017-02-26","2017-05-30"], ["2017-02-26","2017-06-20"]]
    :param airport_departure: the code of the departure airport: i.e "FCO" or "LHR".
    Also it admits multiple airports at the same time: i.e "FCO,LHR"
    :param airport_arrival: code of the arrival airport i.e "BKK" or "KUL" or "BKK,KUL"
    :param extensions: list of the extensions of the kayak domains: i.e ["es", "co.uk", "it", "se"]
    :return: the list of links generated
    '''
    links = []
    for extension in extensions:
        for date in dates:
            link = "https://www.kayak." + extension + "/flights/"+ airport_departure + "-" + airport_arrival + "/" + date[0] + "/" + date[1]
            if "no-return" in link:
                links.append(link[:-9])
            else:
                links.append(link)
    return links


def main(argv):
    month_departure = ''
    day1 = ''
    year_departure = ''
    day2 = ''
    airport_departure = ''
    airport_arrival = ''
    extension = ''
    name=''
    try:
        opts, args = getopt.getopt(argv,"ha:b:y:z:d:r:e:n:",["month-departure=","day1=","year-departure=","day2=","airport-departure=","airport-return=","extension=","name="])
    except getopt.GetoptError:
        print('Options: \n '
              '-e <extension>\n'
              '-a <month-departure>\n'
              '-y <year-departure> \n'
              '-b <day1> \n'
              '-z <day2> \n'
              '-d <airport/s-departure> \n'
              '-r <airport/s-return>\n'
              '-n <filename-to-save>\n\n'
              ' i.e: vuelos.py '
              '-a 10 -y 2017 -b friday -z 00 -d ROM -r MAD -e es -n test.txt')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Options: \n '
                 '-e <extension>\n'
                 '-a <month-departure>\n'
                 '-y <year-departure> \n'
                 '-b <day1> \n'
                 '-z <day2> \n'
                 '-d <airport/s-departure> \n'
                 '-r <airport/s-return>\n'
                 '-n <filename-to-save>\n\n'
                 ' i.e: vuelos.py '
                 '-a 10 -y 2017 -b friday -z 00 -d ROM -r MAD -e es -n test.txt')
            sys.exit()
        elif opt in ("-a", "--month-departure"):
            month_departure = arg
        elif opt in ("-b", "--day1"):
            day1 = arg
        elif opt in ("-y", "--year-departure"):
            year_departure = arg
        elif opt in ("-z", "--day2"):
            day2 = arg
        elif opt in ("-d", "--airport-departure"):
            airport_departure = arg
        elif opt in ("-r", "--airport-return"):
            airport_arrival = arg
        elif opt in ("-e", "--extension"):
            extension = arg
        elif opt in ("-n", "--name"):
            name = arg


    dates = gen_dates(day1,day2,month_departure, year_departure)
    links = gen_links(dates, airport_departure, airport_arrival, extensions=extension.split(","))
    export_list_csv(links,  name)

if __name__ == "__main__":
    main(sys.argv[1:])
