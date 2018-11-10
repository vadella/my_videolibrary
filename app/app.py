import typing
import os

from flask import Flask, render_template
from flask_bootstrap import Bootstrap
import pymongo

from my_videolibrary.my_videolibrary import Movie

MONGO_DB_URL = os.environ.get("MONGO_DB_URL", "127.0.0.1")
MONGO_DB_PORT = int(os.environ.get("MONGO_DB_PORT", 27017))


def create_app():
    app = Flask(__name__)
    app.jinja_env.lstrip_blocks = True
    app.jinja_env.trim_blocks = True
    Bootstrap(app)
    return app


app = create_app()


@app.route("/")
def home():
    return "Hello, Flask!\n"


@app.route("/series/")
def series():
    query_results = get_data()
    movie_summaries = [movie.summary_complete for movie in query_results]

    summaries = {"audio_amount": "audio_summary", "sub_amount": "sub_summary"}
    if movie_summaries:
        header = list(movie_summaries[0].keys())
        # print(movie_summaries[0], header)
        return render_template(
            "series.1.j2",
            query_results=movie_summaries,
            header=header,
            summaries=summaries,
            summaries_values=summaries.values(),
        )


def get_data() -> typing.Sequence[Movie]:
    with pymongo.MongoClient(MONGO_DB_URL, MONGO_DB_PORT) as client:
        db = client.my_videos
        collection_movies = db.movies
        lookup_query = [
            {
                "$lookup": {
                    "from": "audio_tracks",
                    "localField": "movie_id",
                    "foreignField": "movie_id",
                    "as": "audio_tracks",
                }
            },
            {
                "$lookup": {
                    "from": "subtitle_tracks",
                    "localField": "movie_id",
                    "foreignField": "movie_id",
                    "as": "subtitle_tracks",
                }
            },
        ]

        query_results = sorted(
            (
                Movie(movie)
                for movie in collection_movies.aggregate(lookup_query)
            ),
            key=lambda x: x["name"],
        )
        return query_results

if __name__ == "__main__":
    # print("starting")
    app.run(host="0.0.0.0", debug=True)