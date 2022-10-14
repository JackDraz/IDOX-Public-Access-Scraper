
from datetime import date, datetime
from os import replace
import requests
from bs4 import BeautifulSoup
import webbrowser

def get_search_criteria(url):

    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    results = str(soup.find(id="documentType"))

    substrings= []
    writing = False
    for c in results:
        if c == '\"':
            if not writing:
                substrings.append("")
            writing = not writing
        elif writing:
                substrings[-1] += c

    substrings.remove('documentType')
    substrings.remove('documentType')
    substrings.remove('selected')
    substrings.remove('0')
    return substrings

# url = "https://planningpublicaccess.southampton.gov.uk/online-applications/applicationDetails.do?activeTab=documents&keyVal=R4437WOZG5R00"
# page = requests.get(url)
# soup = BeautifulSoup(page.content, "html.parser")
# table = soup.find_all("table", id=("Documents"))

def get_table_items(url):           # When given documents tabs URL from IDOX - extracts set of documents titles/types from site.
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find_all("table", id=("Documents"))
             
    for child in table:             # sorts Table HTML into only text items within children 
        baserow = []
        for tr in child:
            for td in tr:
                if td != "\n":
                    if td != "":
                        try:
                            baserow.append(td.text.replace('\n', ''))
                        except:
                            continue


    try:                            # removes common uneeded values within data, to leave only header row items and row items
        while True:
            baserow.remove("Select this document")
    except ValueError:
        pass

    baserow = list(filter(None, baserow))   # remove any blank values
    amendrow = []
    writing = False                     
    for item in baserow:                # converts all date values to DateTime and creates new list with only date times and info. Assumes first value is date.
        try:
            item = datetime.strptime(item, ("%d %b %Y"))
            writing = True
        except ValueError:
            pass
        if writing == True:
            amendrow.append(item)

    return amendrow


def table_item_dicts(url):
    table_items = get_table_items(url)
    rows = []
    item = table_items.pop(0)  # start with the first element in the list, which we assume to be a DateTime (can check this separately)
    
    while len(table_items) > 0:                 # keep going until the list is empty
        subrow = []
        subrow.append(item)                       # make a new row for this element (always a datetime) and those that follow
        item = table_items.pop(0)               # get the next element, which shouldn't be a date
        while len(table_items) > 0 and not isinstance(item, datetime):   # keep adding elements until we reach a date
            subrow.append(item)
            item = table_items.pop(0)  # when this makes item another datetime, the inner while loop condition will fail and we'll go back to the outer loop and start a new row
        rows.append(subrow)

    return rows
    


# def sort_table_items(url):
#     rows = []
#     for item in get_table_items(url):
#         if item is: 
#             pass

# print(get_search_criteria(url))


# def get_table_docinfo(url): # produces a list of sets 
#     results = []
#     for item in get_table_items(url)[1:]:
#         date = datetime.strptime(item[0:11], ("%d %b %Y"))
#         docinfo = item[11:]
#         results.append([datetime.strftime(date, '%d %b %Y'), docinfo])
#     return results
