from application import app
from flask import Flask, render_template, request
from application.features import *
from application.model import *

songs = pd.read_csv("./CachedData/allsong_data.csv")
complete_feature_set = pd.read_csv("./CachedData/complete_feature.csv")

@app.route("/")
def home():
    return render_template('home.html')


@app.route('/recommend', methods=['POST'])
def recommend():
    URL = request.form['URL']
    df = extract(URL)
    recommendations = recommend_from_playlist(songs, complete_feature_set, df)
    my_songs = []
    for i in range(10):
        song_id = recommendations.iloc[i][1]
        song_name = recommendations.iloc[i][2]
        my_songs.append([song_name, "https://open.spotify.com/track/" + str(song_id)])
    return render_template('results.html',songs= my_songs)