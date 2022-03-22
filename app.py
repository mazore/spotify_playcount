from flask import Flask


class App(Flask):
    def __init__(self):
        super().__init__(__name__)

        self.route('/test', methods=['GET'])(self.test)

    def test(self):
        return 'test'


app = App()

if __name__ == '__main__':
    app.run(debug=True)
