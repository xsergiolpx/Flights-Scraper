import datetime
import sys, getopt
from export_csv import export_list_csv

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

def gen_dates_same_month(month, year):
    '''
    :param month: month to generate dates: ie "03" is march
    :return: something like [['2017-04-04', '2017-04-05'], ['2017-04-04', '2017-04-12']]
    '''
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    all_dates = []
    date = year + "-" + month + "-04"
    #dif = diff_days(date, current_date)
    if diff_days(date, current_date) <= 0: # check that today is before the departure date
        all_dates += [[date, (datetime.datetime.strptime(date, "%Y-%m-%d") + datetime.timedelta(days=x * 7 + 1)).strftime("%Y-%m-%d")] for x in range(0, 5)]
    #if dif > 0 and dif <= 2:

    date = year + "-" + month + "-11"
    if diff_days(date, current_date) <= 0:
        all_dates += [[date, (datetime.datetime.strptime(date, "%Y-%m-%d") + datetime.timedelta(days=x * 7 + 1)).strftime("%Y-%m-%d")] for x in range(0, 4)]

    date = year + "-" + month + "-18"
    if diff_days(date, current_date) <= 0:
        all_dates += [[date, (datetime.datetime.strptime(date, "%Y-%m-%d") + datetime.timedelta(days=x * 7 + 1)).strftime("%Y-%m-%d")] for x in range(0, 3)]

    date = year + "-" + month + "-25"
    if diff_days(date, current_date) <= 0:
        all_dates += [[date, (datetime.datetime.strptime(date, "%Y-%m-%d") + datetime.timedelta(days=x * 7 + 1)).strftime("%Y-%m-%d")] for x in range(0, 2)]

    return all_dates

def gen_dates_different_month(month_departure, month_return, year_departure, year_return):

    '''
    Generates a list of list of dates
    :param month_departure: ie "03"
    :param month_return:  ie "04"
    :return: something like [['2017-03-04', '2017-04-04'], ['2017-04-04', '2017-05-11']]
    '''
    all_dates = []
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    date_departure_base = year_departure + "-" + month_departure + "-04"
    for i in range(0, 5):
        date_departure = datetime.datetime.strptime(date_departure_base, "%Y-%m-%d") + datetime.timedelta(days=i * 7)
        date_return_base = year_return + "-" + month_return + "-04"
        date_departure_full = date_departure.strftime("%Y-%m-%d")
        if diff_days(date_departure_full, current_date) <= 0: # check that today is before the departure date
            all_dates += [[date_departure_full,(datetime.datetime.strptime(date_return_base, "%Y-%m-%d")
                                                            + datetime.timedelta(days=x * 7)).strftime("%Y-%m-%d")] for x in range(0, 5)]
    return all_dates

def gen_dates_no_return(month_departure, year_departure):
    all_dates = []
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    date_departure_base = year_departure + "-" + month_departure + "-04"
    for i in range(0, 5):
        date_departure = datetime.datetime.strptime(date_departure_base, "%Y-%m-%d") + datetime.timedelta(days=i * 7)
        date_departure_full = date_departure.strftime("%Y-%m-%d")
        if diff_days(date_departure_full, current_date) <= 0:  # check that today is before the departure date
            all_dates += [[date_departure_full, "no-return"]]
    return all_dates

def gen_dates(month_departure, month_return, year_departure, year_return):
    '''
    generates the list of lists for departure and return dates
    :param month_departure: i.e "03" for march
    :param month_return: i.e "06" for june
    they have to be str of two characters
    :return: list of lists with possible departure dates and return dates in each element
    i.e [['2017-03-04', '2017-04-04'], ['2017-04-04', '2017-05-11']]
    '''
    if month_departure == month_return and year_departure == year_return:
        return gen_dates_same_month(month_departure, year_departure)
    if month_return == "00":
        return gen_dates_no_return(month_departure, year_departure)
    else:
        return gen_dates_different_month(month_departure, month_return, year_departure, year_return)


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
            link = "https://www.kayak." + extension + "/flights/"+ airport_departure + "-" + airport_arrival + "/" + date[0] + "-flexible/" + date[1] + "-flexible"
            if "no-return" in link:
                links.append(link[:-19])
            else:
                links.append(link)
    return links


def main(argv):
    month_departure = ''
    month_return = ''
    year_departure = ''
    year_return = ''
    airport_departure = ''
    airport_arrival = ''
    extension = ''
    name=''
    try:
        opts, args = getopt.getopt(argv,"ha:b:y:z:d:r:e:n:",["month-departure=","month-return=","year-departure=","year-return=","airport-departure=","airport-return=","extension=","name="])
    except getopt.GetoptError:
        print('Options: \n '
              '-e <extension>\n'
              '-a <month-departure>\n'
              '-y <year-departure> \n'
              '-b <month-return> \n'
              '-z <year-return> \n'
              '-d <airport/s-departure> \n'
              '-r <airport/s-return>\n\n'
              ' i.e: vuelos.py '
              '-a 03 -y 2018 -b 04 -z 2018 -d FCO -r BKK,KUL    (-m2 00 for no return)')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('Options: \n '
                  '-e <extension>\n'
                  '-a <month-departure> \n'
                  '-y <year-departure> \n'
                  '-b <month-return> \n'
                  '-z <year-return> \n'
                  '-d <airport/s-departure> \n'
                  '-r <airport/s-return>\n\n'
                  ' i.e: vuelos.py '
                  '-a 03 -y 2018 -b 04 -z 2018 -d FCO -r BKK,KUL    (-m2 00 for no return)')
            sys.exit()
        elif opt in ("-a", "--month-departure"):
            month_departure = arg
        elif opt in ("-b", "--month-return"):
            month_return = arg
        elif opt in ("-y", "--year-departure"):
            year_departure = arg
        elif opt in ("-z", "--year-return"):
            year_return = arg
        elif opt in ("-d", "--airport-departure"):
            airport_departure = arg
        elif opt in ("-r", "--airport-return"):
            airport_arrival = arg
        elif opt in ("-e", "--extension"):
            extension = arg
        elif opt in ("-n", "--name"):
            name = arg


    dates = gen_dates(month_departure, month_return, year_departure, year_return)
    links = gen_links(dates, airport_departure, airport_arrival, extensions=extension.split(","))
    export_list_csv(links,  name)

if __name__ == "__main__":
    main(sys.argv[1:])