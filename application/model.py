import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from textblob import TextBlob
import re


def generate_playlist_feature(complete_feature_set, playlist_df):
    complete_feature_set_playlist = complete_feature_set[
        complete_feature_set['id'].isin(playlist_df['id'].values)
    ]
    # Find all non-playlist song features
    complete_feature_set_nonplaylist = complete_feature_set[
        ~complete_feature_set['id'].isin(playlist_df['id'].values)
    ]
    
    complete_feature_set_playlist_final = complete_feature_set_playlist.drop(columns = "id")
    return complete_feature_set_playlist_final.sum(axis = 0), complete_feature_set_nonplaylist


def generate_playlist_recos(df, features, nonplaylist_features):
    nonplaylist_features.dropna()
    
    non_playlist_df = df[
        df['id'].isin(nonplaylist_features['id'].values)
    ]
    
    non_playlist_df['sim'] = cosine_similarity(
        nonplaylist_features.drop('id', axis = 1).values, features.values.reshape(1, -1)
    )[:,0]
    
    non_playlist_df_top = non_playlist_df.sort_values(
        'sim',ascending = False
    ).head(10)
    
    return non_playlist_df_top


def recommend_from_playlist(songs, complete_feature_set, playlistDF_test):
    complete_feature_set_playlist_vector, complete_feature_set_nonplaylist = generate_playlist_feature(complete_feature_set, playlistDF_test)
    
    top = generate_playlist_recos(songs, complete_feature_set_playlist_vector, complete_feature_set_nonplaylist)

    return top