import os
import webbrowser
from datetime import datetime
from monitoringmodules import get_search_criteria, get_table_items, table_item_dicts

def get_last_log():
    with open("logdates.json", "r") as l:
        for line in l:
            return datetime.strptime(line, "%Y-%m-%d %H:%M:%S")            

def return_doc_updates(url):
    results_list = table_item_dicts(url)
    last_log = get_last_log()

    for subrow in results_list:
        for item in subrow:
            if isinstance(item, datetime):
                if item > last_log:
                    print(subrow)
            else:
                continue
    

#     webbrowser.open(url)

# with open("logdates.json", "w") as l:
#     today = str(datetime.today().replace(microsecond=0))
#     l.write(today)

# 2022-07-25 10:30:16.963133
# last_log = datetime.strptime(get_last_log(), "%Y-%m-%d %H:%M:%S")
# now = datetime.today().replace(microsecond=0)

# Main function
with open("URL List.txt", 'r') as f:
    for line in f:
        print(table_item_dicts(line))



