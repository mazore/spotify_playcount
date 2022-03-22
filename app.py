from flask import Flask, render_template


class App(Flask):
    def __init__(self):
        super().__init__(__name__)

        self.route('/', methods=['GET'])(self.main_page)

    def main_page(self):
        return render_template('main_page.html')


app = App()

if __name__ == '__main__':
    app.run(debug=True)
