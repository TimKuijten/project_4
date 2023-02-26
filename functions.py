import requests
from bs4 import BeautifulSoup # pip install beautifulsoup4
import pandas as pd
import requests
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import re as re
import time
import pandas as pd
import os
import numpy as np

import pymysql
import sqlalchemy as alch
from getpass import getpass

#import googletrans
from nltk.sentiment.vader import SentimentIntensityAnalyzer
#import spacy

from dotenv import load_dotenv
import re

def get_all_restaurant_data(start, end):
    all_restaurant_data = []
    for offset in range(start, end, 30):
        #Every page shows 30 restaurants
        url = f'https://www.tripadvisor.com/RestaurantSearch-g187497-oa{offset}-Barcelona_Catalonia.html#EATERY_LIST_CONTENTS'
        # As tripadvisor recognized python and blocked it I had to use header User-Agent
        html = requests.get(url, headers={'User-Agent': "Mozilla/5.0"})
        soup = BeautifulSoup(html.content, "html.parser")
        
        tags_name = soup.find_all("a", class_="Lwqic Cj b")
        tags_website = [a.get('href') for a in soup.find_all("a", class_="Lwqic Cj b", href=True)]
        amount_reviews = soup.find_all("span", class_="IiChw")
        tags_rating = soup.find_all("svg", class_="UctUV d H0")
        cuisine_type = soup.find_all("svg", class_="SUszq")

        names = [i.getText().strip() for i in tags_name]
        # As it is a ranking, the output is (rank. Name of restaurant), so we remove the numbers
        names = [re.sub(r'^[^.]*\.', '', name) for name in names]
        website = [i for i in tags_website]    
        reviews = [re.sub(r'\D', '', i.getText().strip()) for i in amount_reviews]
        ratings = [tag.get('aria-label')[:3] for tag in tags_rating]
    

    
        # Zip to add all values in a tuple for each restaurant
        rows = list(zip(names, website, reviews, ratings))
        all_restaurant_data.extend(rows)
        
    df_ta = pd.DataFrame(all_restaurant_data, columns=['Name', 'Website', 'Reviews', 'Rating'])
    return df_ta

def get_restaurant_data(country, start, end):
    # Define df_restaurants inside the function
    df_restaurants = pd.read_csv('df_restaurants.csv')

    restaurant_data = []
    for i in range(len(df_restaurants)):
        url = 'https://www.tripadvisor.{}/{}'.format(country, df_restaurants['Website'][i])
        for offset in range(start, end, 10):
            url = url.replace('Reviews', 'Reviews-or{}'.format(offset))
            html = requests.get(url, headers={'User-Agent': "Mozilla/5.0"})
            soup = BeautifulSoup(html.content, "html.parser")

            # Find the review text and rating
            tag_review = soup.find_all("div", class_="review-container")
            review = [i.find("p", class_="partial_entry").getText().strip() for i in tag_review]
            rating = [int(i.find("span", class_=re.compile("bubble_\d+"))["class"][1][7:]) for i in tag_review]
            restaurant_name_tag = soup.find('h1', {'data-test-target': 'top-info-header'})
            if restaurant_name_tag is not None:
                restaurant_name = restaurant_name_tag.text
            else:
                restaurant_name = np.nan

            # Find the date of visit
            tag_date = soup.find_all("div", class_="prw_rup prw_reviews_stay_date_hsx")
            date = []
            for i in tag_date:
                date_span = i.find("span", class_="stay_date_label")
                if date_span:
                    date_value = date_span.next_sibling.strip()
                else:
                    date_value = np.nan
                date.append(date_value)

            # Extract language and restaurant information
            language = country
            #restaurant = df_restaurants['Name'][i]

            # Zip to add all values in a tuple for each restaurant
            rows = list(zip(review, rating, date, [language]*len(review), [restaurant_name]*len(review)))
            restaurant_data.extend(rows)

    df_ta = pd.DataFrame(restaurant_data, columns=['review', 'rating', 'date', 'language', 'restaurant'])
    return df_ta

def get_restaurant_data2(country, start, end):
    # Define df_restaurants inside the function
    df_restaurants = pd.read_csv('df_restaurants.csv')

    restaurant_data = []
    for i in range(len(df_restaurants)):
        url = 'https://{}.tripadvisor.com/{}'.format(country, df_restaurants['Website'][i])
        for offset in range(start, end, 10):
            url = url.replace('Reviews', 'Reviews-or{}'.format(offset))
            html = requests.get(url, headers={'User-Agent': "Mozilla/5.0"})
            soup = BeautifulSoup(html.content, "html.parser")

            # Find the review text and rating
            tag_review = soup.find_all("div", class_="review-container")
            review = [i.find("p", class_="partial_entry").getText().strip() for i in tag_review]
            rating = [int(i.find("span", class_=re.compile("bubble_\d+"))["class"][1][7:]) for i in tag_review]
            restaurant_name_tag = soup.find('h1', {'data-test-target': 'top-info-header'})
            if restaurant_name_tag is not None:
                restaurant_name = restaurant_name_tag.text
            else:
                restaurant_name = np.nan

            # Find the date of visit
            tag_date = soup.find_all("div", class_="prw_rup prw_reviews_stay_date_hsx")
            date = []
            for i in tag_date:
                date_span = i.find("span", class_="stay_date_label")
                if date_span:
                    date_value = date_span.next_sibling.strip()
                else:
                    date_value = np.nan
                date.append(date_value)

            # Extract language and restaurant information
            language = country
            #restaurant = df_restaurants['Name'][i]

            # Zip to add all values in a tuple for each restaurant
            rows = list(zip(review, rating, date, [language]*len(review), [restaurant_name]*len(review)))
            restaurant_data.extend(rows)

    df_ta = pd.DataFrame(restaurant_data, columns=['review', 'rating', 'date', 'language', 'restaurant'])
    return df_ta
from googletrans import Translator

# create translator object
trans = Translator()

# define a function to translate a review
def translate_review(review):
    try:
        return trans.translate(review).text
    except Exception as e:
        print(f"Translation error: {e}")
        return ""


def add_language_name(dataframe):
    lang_dict = {'ar': 'Arabic', 'CN': 'Chinese', 'DE': 'German', 'EN': 'English', 'FR': 'French', 'COM.GR': 'Greek',
                 'CO.IL': 'Hebrew', 'IN': 'Hindi', 'IT': 'Italian', 'NO': 'Norwegian', 'JP': 'Japanese', 'CO.KR': 'Korean',
                 'NL': 'Dutch', 'PT': 'Portuguese', 'RU': 'Russian', 'SE': 'Swedish', 'TH': 'Thai', 'COM.TR': 'Turkish',
                 'COM.VN': 'Vietnamese'}
    dataframe["Language"] = dataframe["language"].map(lang_dict)
    return dataframe

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
import numpy as np

nltk.download('stopwords')
nltk.download('vader_lexicon')

sia = SentimentIntensityAnalyzer()

def compound(x):
    if x.strip() == "":
        raise ValueError("Input string is empty")
    try:
        return sia.polarity_scores(x)["compound"]
    except Exception as e:
        raise ValueError("Sentiment analysis failed: " + str(e))