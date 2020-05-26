#What is this?
This project is a practice exercise that aims to query the Spotify API and run some basic analysis on the data it extracts from it.
The code authenticates and sends a single query to the Spotify Search API and extracts a sample of tracks that match a wildcard in the track name.
Then it takes 4 values from the results:
- artist(s) - full list of artists listed for the track
- track_name - full name of the track
- track_duration - duration of track (in minutes, not rounded)
- track_popularity - the popularity of the track as ranked by Spotify

The code then reads that same CSV and runs some simple statistics on it and prints the results in the console. 

This is not intended to be used in a production system and is only intended to demonstrate querying an api, creating a CSV from the data and running very simple analysis on that data.

#System Requirements
Written in Python3.7, but should work in other versions with minimal changes needed.

Can be run in pyenv3.7.7.

Packages needed can be installed with the following commands:
```bash
pip install requests
pip install pandas
```

Some python packages exist specifically for the Spotify API, but they are not used here. The Spotify API is queried with standard requests. 

#How to run
Running analyze_tracks.py requires three arguments:
- client_id
- client_secret
- wildcard  - this can be any text, ex. "all by myself", "you win or you die", "crazy in love", etc.

The client_id and client_secret can be obtained from a developer spotify account.
Create an application and generate they ID and Secret here: https://developer.spotify.com/dashboard/applications

Depending on how and where you are running this code, the IDs and wildcard can be passed in a variety of ways.

The id and secret should be stored on the server where they will be run securely and decrypted and passed to the application at the time the code is run.

The wildcard can be user input or input by values stored on the server.

##Helpful links
Spotify's Web API Documentation: https://developer.spotify.com/documentation/web-api/
Pandas User Guide: https://pandas.pydata.org/docs/user_guide
Requests Documentation: https://requests.readthedocs.io/en/master/