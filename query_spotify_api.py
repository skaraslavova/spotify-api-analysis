import datetime
import requests
import base64
from urllib.parse import urlencode

#used to query the spotify api
#requires a client id and a client secret
#more functions can and should be added to this to query artists, albums, etc
#much of this was written with the help of an online spotify api tutorial


class SpotifyAPI(object):
    client_id = None
    client_secret = None
    url = 'https://accounts.spotify.com/api/token'
    access_token = None
    access_token_expires = datetime.datetime.now()
    expired_token = True

    def __init__(self, client_id, client_secret, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client_id=client_id
        self.client_secret=client_secret

    def get_credentails(self):
        client_id = self.client_id
        client_secret = self.client_secret
        if client_id == None or client_secret == None:
            raise Exception("Ooops, you need a client id and client secret.")
        client_creds = f"{client_id}:{client_secret}"
        client_creds_b64 = base64.b64encode(client_creds.encode()) #a base64 encoded string is required

        return client_creds_b64.decode()

    def get_header(self):
        creds_b64 = self.get_credentails()
        return {
            "Authorization": f"Basic {creds_b64}"
        }


    def get_data(self):
        return {
            "grant_type": "client_credentials"
        }

    def handle_auth(self, request):
        token_response_data = request.json()
        now = datetime.datetime.now()
        access_token = token_response_data['access_token']
        expires_in = token_response_data['expires_in']
        expires = now + datetime.timedelta(seconds=expires_in)
        self.access_token = access_token
        self.access_token_expires = expires
        self.expired_token = expires < now

    def perform_auth(self):
        token_url = self.url
        token_data = self.get_data()
        token_headers = self.get_header()
        r = requests.post(token_url, data=token_data, headers=token_headers)
        if r.status_code not in range(200, 299):
            raise Exception("Could not authenticate client.")
        self.handle_auth(r)
        return True

    def get_access_token(self):
        token = self.access_token
        expires = self.access_token_expires
        now = datetime.datetime.now()
        if expires < now:
            self.perform_auth()
            return self.get_access_token()
        elif token == None:
            self.perform_auth()
            return self.get_access_token()
        return token

    def get_resource_header(self):
        access_token = self.get_access_token()
        header = {
            "Authorization": f"Bearer {access_token}"
        }
        return header


    def base_search(self, query_params):
        # not flexible to query a different version of the api, but it can be added as a parameter here
        endpoint = "https://api.spotify.com/v1/search"
        header = self.get_resource_header()
        search_url = f"{endpoint}?{query_params}"
        r = requests.get(search_url, headers=header)
        if r.status_code not in range(200, 299):
            return {}
        return r.json()

    def search(self, query=None, search_type="artist"):

        if query == None:
            raise Exception ("Ooops, a query is required.")

        if isinstance(query, dict):
            query = " ".join([f"{k}:{v}" for k,v in query.items()])

        query_params = urlencode({"q": query, "type": search_type.lower()})

        return self.base_search(query_params)