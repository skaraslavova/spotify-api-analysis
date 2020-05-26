import pandas
import query_spotify_api as spotify_api
import create_csv_of_results as c

#this is a super simple analysis done on data extracted from the spotify api
#we take a user inputted wildcard and query the spotify api for tracks with that name
#in this case, we are not getting an exhaustive list of tracks that match the wildcard as this is a practice exercise
#the default number of tracks we'll get will be 20 and this code does not page through the complete resultset
#we download a CSV with some information extracted from the API and just run a couple of simple stats on that same CSV

#these client id and secret can be set as function instead of globally
client_id = ''
client_secret = ''

#the wildcard can be set separately from the secret and id since they are unlikely to be from the same input
track_wildcard = ''

def calculate_avg_popularity_and_duration(client_id, client_secret, track_wildcard):
    spotify = spotify_api.SpotifyAPI(client_id, client_secret)
    results = spotify.search(query=track_wildcard, search_type="track")
    create = c.CreateCsvOfSongs(track_wildcard, results)
    create.create_csv()
    csv_name = create.csv_name
    df = pandas.read_csv(csv_name)
    avg_popularity = df['track_popularity'].mean()
    total_duration = df['track_duration'].sum().round(1)
    # while the default result count will be 20, it's possible that our wildcard matched fewer than 20 results
    # note that I didn't add a graceful way to tell the user if the wildcard returns 0 matches
    num_tracks = df['track_name'].count()

    return avg_popularity, total_duration, num_tracks

calculations = calculate_avg_popularity_and_duration(client_id, client_secret, track_wildcard)
print(f"The average popularity for a sampling of {calculations[2]} tracks that have \'{track_wildcard}\' in the name is {calculations[0]}.\n"
      f"The total duration for those tracks is {calculations[1]} minutes.")
