import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")

def read_data_from_csv():
    hotels=pd.read_csv('zomato.csv')
    return hotels

#task1: Removing Unwanted Columns
def remove_unwanted_columns():
    hotels=read_data_from_csv()
    remove_cols=['address','phone']
    hotels.drop(remove_cols, axis=1, inplace=True)
    return hotels

#task2: Renaming and Selecting Columns in a Dataset
def rename_columns():
    hotels = remove_unwanted_columns()   
    hotels= hotels.rename(columns={'rate':'rating','approx_cost(for two people)':'approx_cost','listed_in(type)':'type'})
    hotels=hotels[['name','online_order', 'book_table','rating','votes','location','rest_type', 'dish_liked','cuisines','approx_cost','type']]
    return hotels


#task3: handle  null values of each column
def null_value_check():
    hotels=rename_columns()
    hotels= hotels.dropna(subset=['name'])
    hotels['online_order'].fillna(value='NA', inplace=True)
    hotels['book_table'].fillna(value='NA', inplace=True)
    hotels['rating'].fillna(value=0, inplace=True)
    hotels['votes'].fillna(value=0, inplace=True)
    hotels['location'].fillna(value='NA', inplace=True)
    hotels['rest_type'].fillna(value='NA', inplace=True)
    hotels['dish_liked'].fillna(value='NA', inplace=True)
    hotels['cuisines'].fillna(value='NA', inplace=True)
    hotels['approx_cost'].fillna(value=0, inplace=True)
    hotels['type'].fillna(value='NA', inplace=True)
    return hotels


#task4 #find duplicates in the dataset
def find_duplicates():
    hotels=null_value_check()
    hotels=hotels.drop_duplicates(keep='first')
    return hotels


#task5 removing irrelevant text from all the columns
def removing_irrelevant_text():
    hotels= find_duplicates()
    text = r'\b(Rated|RATED)\b'

    cols = ['name','online_order', 'book_table', 'rating', 'votes', 'location','rest_type', 'dish_liked', 'cuisines', 'approx_cost', 'type']
    for col in cols:
        hotels = hotels[~hotels[col].astype(str).str.contains(text, regex=True)]
        hotels = hotels[~(hotels == 0).any(axis=1)]
    hotels = hotels.dropna()

    return hotels


#task6: check for unique values in each column and handle the irrelevant values
def check_for_unique_values():
    hotels=removing_irrelevant_text()
    hotels = hotels[hotels['online_order'].isin(['Yes', 'No'])]
    hotels['rating'] = hotels['rating'].replace(['NEW', '-'], 0)
    hotels['rating'] = hotels['rating'].str.replace('/5', '')
    hotels['rating'] = hotels['rating'].fillna(0)

    return hotels


#task7: remove the unknown character from the dataset and export it to "zomatocleaned.csv"
def remove_the_unknown_character():
    dataframe=check_for_unique_values()
    dataframe['name']=dataframe['name'].str.replace('[Ãx][^A-Za-z]+','',regex=True)
    #export cleaned Dataset to newcsv file named "zomatocleaned.csv"
    dataframe.to_csv('zomatocleaned.csv')
    return dataframe


#Next is to create table on phpMyAdmin (lOGIN with db.py) with named "zomato"  use final dataset after cleaning for dedupliction to upload on the provided database for performing analysis in  MySQL. 
#To Run this task first Run the appliation for Terminal to create table named 'Zomato' and then run test.
def start():
    remove_the_unknown_character()

def task_runner():
    start()
