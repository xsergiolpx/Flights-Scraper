import pandas as pd
import glob
import sys

def analyze(folder, order="price"):
    # Print all the string
    pd.options.display.max_colwidth = 200

    # Load all files
    allFiles = glob.glob(folder + "*tmp*.csv")

    frame = pd.DataFrame()
    list_ = []
    for file_ in allFiles:
        df = pd.read_csv(file_,index_col=None, header=0, sep=";")
        list_.append(df)
    frame = pd.concat(list_)

    '''
    def currency_type(row):
        if ".es" in row['link']:
            val = row["price"]
        elif ".co.uk" in row['link']:
            val = round(row["price"]*1.17)
        else:
            val = row["price"]
        return val

    frame['price'] = frame.apply(currency_type, axis=1)
    '''

    #frame.loc[frame["link"].str.contains(".es"),]["currency"] = "eur"
    frame = frame.sort_values(order)
    frame = frame.reset_index(drop=True)
    print(frame.head(n=15))
    frame.to_csv(folder + "results.csv", sep=";")
    frame.to_html(folder + "results.html")


# Create the analysis
folder = sys.argv[1]
analyze(folder=folder)
