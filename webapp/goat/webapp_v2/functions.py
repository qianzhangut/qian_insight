# -*- coding: utf-8 -*-
"""
Created on Wed Sep 26 16:52:17 2018
@author: Graccolab
"""


import os
from wordcloud import WordCloud
import datetime
import pandas as pd
#import cv2
import matplotlib.pyplot as plt

from nltk.probability import FreqDist
import nltk
from wordcloud import WordCloud

from joblib import dump, load
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from sklearn.ensemble import RandomForestRegressor



def create_word_cloud(player_name):
	df = pd.read_csv('/home/ubuntu/webapp_v2/static/data/cloud_data_spacy.csv')
	text = df.joint_tweets.loc[df.name == player_name]
	try:
		token = nltk.word_tokenize(text.values[0])
		fdist = FreqDist(token)
		tops=fdist.most_common(30)
		text_cloud = [tops[i][0] for i in range(len(tops))]

		text_plot = ' '.join([i for i in text_cloud])

		lo = nltk.word_tokenize(player_name)
		pl = [lo[0], lo[-1], lo[-1].lower(), lo[0].lower()]
		stop = ['thi', 'come', 'don', 'citi', 'app', 'andi', 'onli', 'player', 'play', 'fuck']
		stopwords = stop + pl

		wordcloud = WordCloud(width = 960, height = 600, 
					background_color ='white', margin=10, prefer_horizontal=1,
					stopwords = stopwords,
					normalize_plurals=False, min_font_size = 20).generate(text_plot) 
		file_name= player_name +'.png'
		file_path='/home/ubuntu/webapp_v2/static/img/player/' + file_name
		wordcloud.to_file(file_path)
	except IndexError:
		file_name = 'sorry.jpg'
	return file_name


def value_predict(player_name):
	aa=[]
	name = pd.read_csv('/home/ubuntu/webapp_v2/static/data/webapp_name.csv')
	clf = load('/home/ubuntu/webapp_v2/static/data/train.joblib')

	data = pd.read_csv('/home/ubuntu/webapp_v2/static/data/final129_orig.csv')

	try:
		name_id = name[name['name'] == player_name ].index.tolist()[0]

		part1 = data[['best', 'goal', 'good', 'great',
			   'love', 'foot_both', 'foot_left', 'foot_right', 'position_Defender',
			   'position_Forward', 'position_Goalkeeper', 'position_Midfielder',
			   'outfitter_Nike', 'outfitter_adidas', 'outfitter_other',
			   'nationality_ver2_Africa', 'nationality_ver2_Asia',
			   'nationality_ver2_Europe', 'nationality_ver2_North America',
			   'nationality_ver2_Oceania', 'nationality_ver2_South America']]
		part2 = data[['height_ver2','injury_ver2', 'join_date_ver2', 'exp_date_ver2', 'sent_score', 'sent_max', 'sent_min', 'age',
			   'startelfquote', 'minutenquote', 'Player_agent_ver2', 'appearance_ver2',
			   'minutes_ver2', 'num_tweets_ver2', 'following_ver2', 'followers_ver2',
			   'likes_ver2', 'date_joined_twitter_ver3', 'goals_ver2', 'Assists_ver2',
			   'min_per_goal_ver2', 'market_value_ver2']]

		mm = MinMaxScaler()

		part2_scaled = mm.fit_transform(part2)
		final_data = np.concatenate((part1.to_numpy(), part2), axis=1)

		X = final_data[:, :-1]

		value = clf.predict(X)

		injury = 'Yes' if data['injury_ver2'].loc[name_id] == 1 else 'No'
		aa = [np.around(value[name_id], decimals=1), int(data['followers_ver2'].loc[name_id]), int(data['goals_ver2'].loc[name_id]), \
				injury , data['age'].loc[name_id], int(data['sent_score'].loc[name_id])]
		
	except IndexError:
		aa = ['\u221e']*6

	return aa


