from flask import Flask, render_template, request, escape
from vsearch import search4letters
import mysql.connector

"""Creating a Flask Webapp Object"""
app = Flask(__name__)


def log_request(req: 'flask_request', res: str) -> None:
    dbconfig = {'host': '127.0.0.1', 'user': 'vsearch', 'password': 'vsearchpasswd', 'database': 'vsearchlogDB',}
    conn = mysql.connector.connect(**dbconfig)
    cursor = conn.cursor()
    _SQL = """insert into log (phrase, letters, ip, browser_string, results) values (%s, %s, %s, %s, %s)"""
    cursor.execute(_SQL, (req.form['phrase'], req.form['letters'], req.remote_addr, 'TempleBrowser', res, ))
    conn.commit()
    cursor.close()
    conn.close()


@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    """Return result of request at the html form"""
    phrase = request.form['phrase']
    letters = request.form['letters']
    results = str(search4letters(phrase, letters))
    log_request(request, results)
    title = 'Here are your results:'
    return render_template('result.html', the_title=title, the_phrase=phrase, the_letters=letters,
                           the_results=results, )


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    """Create html form for user from 'entry.html' with the_title as JiniaII argument"""
    return render_template('entry.html', the_title='Welcome')


@app.route('/viewlog')
def view_the_log() -> 'html':
    result_list = []
    with open('vsearch.log') as log:
        for line in log:
            line = escape(line)
            result_list.append(line.split('|'))
    titles = ('Form Data', 'Remote_addr', 'User_agent', 'Results')
    return render_template('viewlog.html', the_title='View log', the_data=result_list, the_row_titles=titles,)


if __name__ == '__main__':
    """Debugging mode"""
    app.run(debug=True)
