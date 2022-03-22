from flask import Flask, render_template, request
from spotify_api import SpotifyAPI


class App(Flask):
    def __init__(self):
        super().__init__(__name__)

        self.api = SpotifyAPI()

        self.route('/', methods=['GET'])(lambda: render_template('main_page.html'))
        self.route('/album', methods=['GET'])(self.album)

    def album(self):
        id = request.args.get('id')
        return self.api.get_playcounts_of_album(id)


app = App()

if __name__ == '__main__':
    app.run(debug=True)
