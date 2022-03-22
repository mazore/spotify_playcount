from bs4 import BeautifulSoup
import json
import requests


class SpotifyAPI:
    def __init__(self):
        self.headers = {'authorization': f'Bearer {self.get_bearer_token()}'}

    def get_bearer_token(self):
        response = requests.get('https://open.spotify.com')
        soup = BeautifulSoup(response.text, 'html.parser')
        element = soup.find_all(id='config')[0]
        return json.loads(element.text)['accessToken']

    def get_search_result_id(self, search: str):
        """Gets the id of the top search string specified.
        """
        url = 'https://api-partner.spotify.com/pathfinder/v1/query'
        shahash = 'c66c4f0d8d7f47e0dd4a6b5267c5b1197a226197f57d9c20aca5cba8d274f954'
        params = {
            'operationName': 'searchDesktop',
            'variables': json.dumps({'searchTerm': search, 'offset': 0, 'limit': 10, 'numberOfTopResults': 1}),
            'extensions': json.dumps({'persistedQuery': {'version': 1, 'sha256Hash': shahash}})
        }
        resp = requests.get(url, params=params, headers=self.headers)
        if 'data' not in resp.json():
            raise ValueError('Invalid response: ' + resp.text)

        return resp.json()['data']['search']['topResults']['items'][0]['uri'].split(':')[-1]

    def get_albums_of_artist(self, artist_id):
        """Gets all album ids for the artist specified.
        """
        url = 'https://api-partner.spotify.com/pathfinder/v1/query'
        shahash = 'e38c23e4e8aa873903ab47c2c84ab9f1175e645cf03a34eafdeea07454e5c3da'
        params = {
            'operationName': 'queryArtistDiscographyAlbums',
            'variables': json.dumps({'uri': f'spotify:artist:{artist_id}', 'offset': 0, 'limit': 50}),
            'extensions': json.dumps({'persistedQuery': {'version': 1, 'sha256Hash': shahash}})
        }
        resp = requests.get(url, params=params, headers=self.headers)
        if 'data' not in resp.json():
            raise ValueError('Invalid response: ' + resp.text)

        ids = []
        for item in resp.json()['data']['artist']['discography']['albums']['items']:
            id = item['releases']['items'][0]['id']
            ids.append(id)
        return ids

    def get_playcounts_of_album(self, album_id):
        """Returns a dict like {song_title: playcount, ...} for the album specified.
        """
        url = 'https://api-partner.spotify.com/pathfinder/v1/query'
        shahash = '3ea563e1d68f486d8df30f69de9dcedae74c77e684b889ba7408c589d30f7f2e'
        params = {
            'operationName': 'queryAlbumTracks',
            'variables': json.dumps({'uri': f'spotify:album:{album_id}', 'offset': 0, 'limit': 300}),
            'extensions': json.dumps({'persistedQuery': {'version': 1,'sha256Hash': shahash}})
        }
        resp = requests.get(url, params=params, headers=self.headers)
        if 'data' not in resp.json():
            raise ValueError('Invalid response: ' + resp.text)

        playcounts = {}
        for track in resp.json()['data']['album']['tracks']['items']:
            name = track['track']['name']
            playcount = int(track['track']['playcount'])
            playcounts[name] = playcount
        return playcounts


# Example usage
if __name__ == '__main__':
    api = SpotifyAPI()
    artist_id = api.get_search_result_id('kanye')  # Gets Kanye's artist id

    ids = api.get_albums_of_artist(artist_id)  # Gets album ids for kanye

    all_playcounts = {}
    for album_id in ids:
        album_playcounts = api.get_playcounts_of_album(album_id)
        all_playcounts.update(album_playcounts)
    all_playcounts = [(k, v) for k, v in sorted(all_playcounts.items(), key=lambda x: x[1])]

    for playcount, song_title in all_playcounts:
        print(f'{playcount:,}', song_title)
