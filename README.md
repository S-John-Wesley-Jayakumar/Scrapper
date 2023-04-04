Twitter Data Scraper

This is a Python script for scraping tweets from Twitter using the snscrape package and displaying them on a Streamlit app. The app also includes the option to save the scraped data to a MongoDB database and download the data in CSV or JSON format.
Requirements

This script requires the following Python packages to be installed:
•	streamlit
•	pandas
•	pymongo
•	snscrape


How to use

1.	Make sure all the required packages are installed.
2.	Replace the username, password, host, port, and database values in line 9 with the appropriate values for your MongoDB database.
3.	Run the script by running the following command in the terminal:
4.	Input the search keyword, start date, end date, and the number of tweets to scrape in the Streamlit app.
5.	Click the "Scrape" button to scrape the Twitter data.
6.	Click the "Save to MongoDB" button to save the scraped data to a MongoDB database.
7.	Click the "Download as CSV" or "Download as JSON" button to download the scraped data in the desired format.


Functions


scrape_tweets(keyword, start_date, end_date, tweet_limit)

  This function scrapes Twitter data based on the given search keyword, start_date, end_date, and the tweet_limit (the number of tweets to scrape). 
It returns a list of dictionaries containing the following tweet information:
•	date: the date of the tweet
•	id: the ID of the tweet
•	url: the URL of the tweet
•	content: the text content of the tweet
•	user: the username of the tweet author
•	reply_count: the number of replies to the tweet
•	retweet_count: the number of retweets of the tweet
•	language: the language of the tweet
•	source: the source of the tweet (e.g. Twitter Web App, Twitter for iPhone)
•	like_count: the number of likes of the tweet

download_dataframe(df, format='csv', file_name='data')

  This function converts the given dataframe df to either CSV or JSON format, and downloads the resulting file with the given file_name.
Streamlit App Code
The Streamlit app code is divided into three sections:
1.	Get user inputs
2.	Scrape Twitter data
3.	Save scraped data to MongoDB and download the data

Get user inputs

  This section allows the user to input the search keyword, start_date, end_date, and the tweet_limit.
  
Scrape Twitter data

  This section includes a "Scrape" button that calls the scrape_tweets function and displays the resulting data in a pandas dataframe.
  
Save scraped data to MongoDB and download the data

  This section includes a "Save to MongoDB" button that calls the scrape_store function to save the scraped data to a MongoDB database. 
It also includes a "Download as CSV" and "Download as JSON" button that calls the download_dataframe function to download the scraped data in the desired format.

