import pandas as pd

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=['GET'])
def home():
    df_ratings = pd.read_csv('../data/ratings.csv')

    genre_cols = [col.replace('genre_', '') for col in df_ratings.columns if col.startswith('genre_')]

    genre = request.args.get('genre', None)
    sort_by = request.args.get('sort', None)
    votes_threshold = int(request.args.get('threshold', '0'))

    # Sort dataframe
    if sort_by:
        if sort_by == 'rate':
            df_ratings = df_ratings.sort_values(['rate', 'votes'], ascending=False)
        if sort_by == 'votes':
            df_ratings = df_ratings.sort_values(['votes', 'rate'], ascending=False)

    # Filter by genre
    if genre:
        df_ratings = df_ratings[df_ratings[f'genre_{genre}'] == 1]

    # Filter by quantity of votes
    df_ratings = df_ratings[df_ratings['votes'] > votes_threshold]

    return render_template("home.html", df_animes=df_ratings.head(100), genres=genre_cols)

if __name__ == '__main__':
    flask_options = dict(
        debug=True,
    )
    app.run(**flask_options)