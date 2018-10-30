from flask import Flask, render_template
import pymongo

from flask_bootstrap import Bootstrap


def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    return app


app = create_app()


@app.route("/")
def home():
    # print(repr(get_data()))
    return "Hello, Flask!\n" + repr(get_data())


@app.route("/series/")
def series():
    columns_video, columns_audio, query_results = get_data()
    return render_template(
        "series.1.j2",
        columns_audio=columns_audio,
        columns_video=columns_video,
        query_results=query_results,
    )


def get_data():
    with pymongo.MongoClient() as client:
        db = client.my_videos
        collection_videos = db.videos
        lookup_query = [
            {
                "$lookup": {
                    "from": "audio_tracks",
                    "localField": "video_id",
                    "foreignField": "video_id",
                    "as": "audio_tracks",
                }
            }
        ]
        columns_video = ("title", "duration")
        columns_audio = ("name", "language", "codec_id", "channels")

        query_results = list(collection_videos.aggregate(lookup_query))
        # print(query_results)
        return (columns_video, columns_audio, query_results)
