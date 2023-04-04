import streamlit as st
import pandas as pd
import pymongo
import snscrape.modules.twitter as sntwitter
from datetime import datetime, timedelta
import base64
import io
import csv
import json

# Connect to MongoDB database with mongo db connection string
client = pymongo.MongoClient("mongodb://<username>:<password>@<host>:<port>/<database>")
db = client["newtwitter_db"]
col = db["newtwitter_collection"]


#Scrape_tweets function scrapes twitter data and displays the data in the streamlit app


def scrape_tweets(keyword, start_date, end_date, tweet_limit):

    tweets = []

    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f"{keyword} since:{start_date} until:{end_date}").get_items()):
        if i >= tweet_limit:
            break
        tweets.append({
            "date": tweet.date,
            "id": tweet.id,
            "url": tweet.url,
            "content": tweet.content,
            "user": tweet.user.username,
            "reply_count": tweet.replyCount,
            "retweet_count": tweet.retweetCount,
            "language": tweet.lang,
            "source": tweet.sourceLabel,
            "like_count": tweet.likeCount
        })

    return tweets

# Scrape_store scrapes data and stores scrapped data as well as additional information like tweets length in mongo db which are used for querying later

def scrape_store(keyword, start_date, end_date, tweet_limit):
    tweets_Data= []

    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f"{keyword} since:{start_date} until:{end_date}").get_items()):
        if i >= tweet_limit:
            break
        tweets_Data.append({
            "date": tweet.date,
            "id": tweet.id,
            "url": tweet.url,
            "content": tweet.content,
            "user": tweet.user.username,
            "reply_count": tweet.replyCount,
            "retweet_count": tweet.retweetCount,
            "language": tweet.lang,
            "source": tweet.sourceLabel,
            "like_count": tweet.likeCount
        })

    return tweets_Data


# Download_dataframe function converts the twitter data frame to JSON  and  CSV  file formats

import codecs

def download_dataframe(df, format='csv', file_name='data'):
    
    if format == 'csv':
        data = df.to_csv(index=False)
        file_extension = '.csv'
        st.write("Click on the link to download")
    elif format == 'json':
        data = df.to_json(orient='records')
        file_extension = '.json'
        
        st.write("Click on the link to download")
    else:
        raise ValueError(f"Unsupported format: {format}")
    

    stream = io.StringIO(data)
    
    # Encode the stream as bytes
    bytes_data = stream.getvalue().encode('utf-8')
    
    # Create a download button that opens the file in a new tab

    b64 = base64.b64encode(bytes_data).decode()

    href = f'<a href="data:file/{file_extension};base64,{b64}" target="_blank" download="{file_name}{file_extension}">Scrapped_data {file_extension.upper()}</a>'
    st.markdown(href, unsafe_allow_html=True)


 


# Streamlit app code
   

def app():
    tweets1 = []
    df = pd.DataFrame()

    d = []

    st.title("Twitter Data Scraper")

    # Get user inputs
    keyword = st.text_input("Enter a keyword or hashtag to search")
    start_date = st.date_input("Select the start date")
    end_date = st.date_input("Select the end date")
    tweet_limit = st.number_input("Enter the number of tweets to scrape")

    # Scrape Twitter data

    if st.button("Scrape"):
        tweets1 = scrape_tweets(keyword, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"), tweet_limit)

        # Display Twitter data
        if len(tweets1) > 0:
            df = pd.DataFrame(tweets1)
            st.write(df)
        else:
            st.warning("No tweets found")


     # scrape and store the data

    if st.button("Save to MongoDB"):
        
        tweets_store = scrape_store(keyword, start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"), tweet_limit)

            
        data = {
            "Scraped Word": keyword,
            "Scraped Date": datetime.now(),
            "Start Date":start_date.strftime("%Y-%m-%d"),
            "End Dtae":end_date.strftime("%Y-%m-%d"),
            "length":tweet_limit,
            "Scraped Data": tweets_store
        }
        col.insert_one(data)        
        
        st.write(type(data))

        st.success("Data saved to MongoDB")


    #Query the data stored in mongo db and  returns the data as dataframe

    def q():
        
        # Mongo db query
        query = {"$and": [{"Scraped Word": keyword,}, {"Start Date":start_date.strftime("%Y-%m-%d")},{"End Dtae":end_date.strftime("%Y-%m-%d")} ,{"length":tweet_limit}]}

        cursor = db["newtwitter_collection"].find(query)

        data = (cursor)
     
        d = data[0]["Scraped Data"]

        df1 = pd.DataFrame(d)

        return df1

    # if else for downloading the data in user preferred format

    if st.button("Download as json "):
        #calling query function to fetch thedta from mongo db
        s = q()        

        #converting dataframe to json format
        download_dataframe(s, format='json', file_name='scrapped_data_json')


    if st.button("Download as csv "):  
            #calling query function to fetch the data from mongo db and store its values as a dataframe
            t = q()  

            #converting dataframe to csv format          
             
            download_dataframe(t, format='csv', file_name='scrapped_data_csv') 


#driver code

app()
