import pandas as pd
import time
import re

#used to create a CSV with the results from an api request
#would add to this to query more results - currently just gets the first results from the api and writes the CSV
#in practice, we would want to to go through the next cursor so we download all of the results from the API

class CreateCsvOfSongs(object):
    track_wildcard = None
    results = None
    csv_name = None

    def __init__(self, track_wildcard, returned_results, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.track_wildcard = track_wildcard #this can be any keyword
        self.results = returned_results

    def create_df_of_songs(self):
        track_name = []
        duration = []
        popularity = []
        artists_for_track = []

        for result in self.results['tracks']['items']:
            artists = result['artists']
            #more than one artist can be listed for a track, so we want to create a comma separated list
            #this could get quite long and might need to be truncated
            artist_name = []
            for artist in artists:
                artist_name.append(artist['name'])
            artist_names = ", ".join(artist_name)
            artists_for_track.append(artist_names)
            track_name.append(result['name'])
            #converting the duration in ms to minutes - not doing the rounding here in case more precise data is needed
            duration.append((result['duration_ms']/(1000*60))%60)
            popularity.append(result['popularity'])

        t_df = pd.DataFrame({"artist(s)": artists_for_track, "track_name": track_name, "track_duration": duration,
                             "track_popularity": popularity})
        return t_df

    def create_csv(self):
        #make sure that the csv name is clean and unique by removing characters and adding a timestamp to the filename
        csv_name = re.sub('[^a-zA-Z0-9\n\.]', '_', self.track_wildcard) + str(time.time()) + ".csv"
        self.csv_name=csv_name
        t_df = self.create_df_of_songs()
        t_df.to_csv(csv_name)
