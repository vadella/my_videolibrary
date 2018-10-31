from flask import Flask, render_template
import pymongo
import typing
from flask_bootstrap import Bootstrap

from my_videolibrary.my_videolibrary import Movie


def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    return app


app = create_app()


@app.route("/")
def home():
    return "Hello, Flask!\n" + repr(get_data())


@app.route("/series/")
def series():
    query_results = get_data()
    movie_summaries = [movie.summary_complete for movie in query_results]

    summaries = {"audio_amount": "audio_summary", "sub_amount": "sub_summary"}
    if movie_summaries:
        header = list(movie_summaries[0].keys())
        print(movie_summaries[0], header)
        return render_template(
            "series.1.j2",
            query_results=movie_summaries,
            header=header,
            summaries=summaries,
            summaries_values=summaries.values(),
        )


def get_data() -> typing.Sequence[Movie]:
    with pymongo.MongoClient() as client:
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
            (Movie(movie) for movie in collection_movies.aggregate(lookup_query)),
            key=lambda x: x["name"]
        )
        return query_results
