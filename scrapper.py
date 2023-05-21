# Import required libraries
from bs4 import BeautifulSoup
import numpy as np
import requests

# Get the html contents of the web page to scrape
source = requests.get('https://www.faballey.com/clothing/women-tops/cat?depth=2&label=clothing-tops&page=1')

# Give the content to the BeautifulSoup library to scrape the data
soup = BeautifulSoup(source.content, 'html.parser')

# Find the <ul> tag which have the items of cloths as list
ul = soup.find(id='JsonProductList')

count=0
all_items = []      # Stores all the items

# Iterate the products present in the web page
for li in ul.find_all('li'):

    # Get the title from the <p> tag
    title = li.find_all(class_='catgName')[0].find('p').string

    # Get the link from the <a> tag
    link = "https://www.faballey.com"+li.find('a')['href']

    # Get the html content of the particular product to get the description
    source_in = requests.get(link)
    soup_in = BeautifulSoup(source_in.content, 'html.parser')

    # Get the description from the corresponding div
    desc_div = soup_in.find('div', class_='prodecCntr')
    contlist = desc_div.find_all('div', class_='predection-content')

    des = []    # Stores all desc data

    # Iterate to get description and details
    for i in range(len(contlist)-1):
        cont = contlist[i]

        all_desc = cont.find_all('p')

        # This if statement is to overcome the error in finding <p> tags.
        if(len(all_desc) > 1):
            if(all_desc[1].contents[0].startswith("Please")):
                break
            des.append(all_desc[1].contents)

        else:
            des.append(all_desc[0].contents)


    des_str = ""    # Final description string

    # Add the content to the final desc string "des_str"
    for i in range(0, len(des[0]), 2):
            des_str+= des[0][i] + " "
    if(len(des)>1):
        for i in range(0, len(des[1]), 2):
            des_str+= des[1][i] + " "
    
    item_list = [title, des_str, link]

    count+=1
    print(count, " - ", title, " - ", link, "\n")
    
    # Append items to all items list
    all_items.append(item_list)

# Convert it to numpy array to check the shape of the list
num_arr = np.array(all_items)
print("Shape ", num_arr.shape)

# CSV Writing (To store the data into an csv file)
import csv

fields = ['title', 'desc', 'link']

filename = "dataset.csv"
with open(filename, 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fields)
    csvwriter.writerows(all_items)

print('\nDone')