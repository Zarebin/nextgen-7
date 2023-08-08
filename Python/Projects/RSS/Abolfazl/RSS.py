#!/usr/bin/python3
import feedparser, feedfinder2, requests, csv
from urllib.parse import urlparse
import collections
import os
import sched, time
from timeout_decorator import timeout
import concurrent.futures
scheduler = sched.scheduler(time.time, time.sleep)

def extract_domain(link):
    if not 'https' in link:
        link = "https://" + link
    parsed_url = urlparse(link)
    domain = parsed_url.netloc.split(":")[0]
    return domain

@timeout(10)
def is_existing_address(website):
    try:
        if not 'http' in website.lower():
            website = 'http://' + website
        response = requests.get(website)
        if response.status_code == 200:
            return True
        else:
            return False
    except requests.exceptions.RequestException:
        return False

@timeout(20)
def rss_finder(website):
    try:
        url = feedfinder2.find_feeds(website)[0]
        print("The RSS of {} founded!".format(extract_domain(website)))
        return url
    except:
        return False

def find_news(rss_link):
    try:
        NewsFeed = feedparser.parse(rss_link)
        links = []
        for entry in NewsFeed.entries:
            links.append(entry['link'])
        return links
    except:
        return False

def csv_of_links(links, website):
    try:
        file_path =  str(extract_domain(website)) + ".csv"

        if not os.path.exists(file_path):
            with open(file_path, 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                for link in links:
                    csvwriter.writerow([link])
            print(file_path + " created!")
            return len(links)


        else:
            counter = 0
            something_new = False
            with open(file_path, 'r', newline='') as csvfile:
                csvreader = csv.reader(csvfile)
                existing_links = set()
                for row in csvreader:
                    existing_links.update(row)


                for link in links:
                    if link not in existing_links:
                        existing_links.add(link)
                        something_new = True
                        counter += 1

            with open(file_path, 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                for link in existing_links:
                    csvwriter.writerow([link])
            if something_new:
                print(file_path + " is updated!")
                return counter
            else:
                print("Nothing new added to " + file_path)
                return 0

    except:
        print("Something went wrong in creating csv file for the {}:( ".format(file_path))
        return 0

def collect_links(address, rss_link):
    global scheduler
    
    news_links = find_news(rss_link)
    if news_links != False:
        news_numbers = csv_of_links(news_links, address)
        
        if news_numbers < 10:
            update_interval = 1800  
        else:
            update_interval = 900  
            
        scheduler.enter(update_interval, 1, collect_links, (address, rss_link,))
        print("The next update will be in {} seconds later for site {} :) ".format(update_interval
                                                                                        , address))
        return news_numbers

def show_addresses(addresses, message):
    print(message + "\n[\n")
    for address in addresses:
        print("\t" + address)
    print("]\n********")

def give_addresses(accepted_addresses):
    give_address = True
    addresses = []
    while give_address:
        address = input("Please enter the website or it's rss link and enter 0 to exit :)")
        if address == '0':
            print("Let's GO!")
            give_address = False
        else:
            try:
                flag = is_existing_address(address)
                if not flag:
                    print(address + " is not a website or cannot be accessed!")
                else:
                    addresses.append(address)
            except:
                print(address + " is not a website or cannot be accessed!")
                
        show_addresses(accepted_addresses + addresses, "The addresses which you entered untill now are:")
    
    return addresses

def create_and_update_csv_files(my_news):
    for news in my_news:
        collect_links(news.website, news.rss_link)
    
    scheduler.run()


news = collections.namedtuple('news', ['website', 'rss_link'])
my_news = []
rss_links = []
broken_rss_addresses = []
accepted_addresses = []
give_address = True

while give_address != '0':
    addresses = give_addresses(accepted_addresses)

    for address in addresses:
        try:
            rss_link = rss_finder(address)
            
            if rss_link != False and not rss_link in rss_links:
                my_news.append(news(extract_domain(address), rss_link))
                rss_links.append(rss_link)
                accepted_addresses.append(extract_domain(address))
            else:
                broken_rss_addresses.append(address)
        except:
            broken_rss_addresses.append(address)

        
    show_addresses(broken_rss_addresses, "The addresses which their rss cannot be found:") 
    show_addresses(accepted_addresses , "The addresses which you entered untill now are:")
    

    give_address = input("You can continue by pressing 0 or give another addresses by pressing any key:")
    broken_rss_addresses = []

if len(my_news) != 0:
    create_and_update_csv_files(my_news)
    
    
print("Bye :) ")
