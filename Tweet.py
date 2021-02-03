
import tweepy

import csv

import mysql.connector

import twitterkeys as cfg

import pandas as pd


  


def easy():
    auth = tweepy.OAuthHandler(cfg.twitter["consumer_key"], cfg.twitter["consumer_secret"])
    auth.set_access_token(cfg.twitter["access_key"], cfg.twitter["access_secret"])
    api = tweepy.API(auth)
           
    tagb=input('Enter the word you want search in twitter: ')


    tags = tagb.split(sep=",")
        


    class StreamListener(tweepy.StreamListener):

        def on_status(self, status):
            print(status.id_str)
            if status.retweeted:
                return
            name = status.user.screen_name
            created = status.created_at    
            loc = status.user.location
            coords = status.coordinates
            followers = status.user.followers_count
            description = status.user.description
            text_ = status.text
            
            #Connected to mysql DB using conf file
            con = mysql.connector.connect(option_files='my.conf')

            cursor = con.cursor(buffered=True)
            fd = open('tweetquery.sql', 'r')
            sqlFile = fd.read()
            fd.close()

            # all SQL commands (split on ';')
            sqlCommands = sqlFile.split(';')

            # Execute every command from the input file
            for command in sqlCommands:
                cursor.execute(command, (name, created, loc, coords, followers, description, text_))
    
            try:
                con.commit()

                    
            except:
                con.rollback()
            
            con.close()

        def on_error(self, status_code):
            if status_code == 420:
              
                return False

    streamListener = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=streamListener,tweet_mode='extended')
    stream.filter(track=tags)


if __name__ == '__main__':
    easy()




   

