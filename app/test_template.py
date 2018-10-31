from jinja2 import Template
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape(["html", "xml"]),
)
template = env.get_template("series.2.j2")

query_results = [
    {
        "name": "West Side Story",
        "year": "1961",
        "duration": "2:52:55",
        "display_width": 1928,
        "display_height": 880,
        "codec_id": "V_MPEG4/ISO/AVC",
        "location": "\\\\OnzeNas\\FILM_Eigen\\West Side Story (1961)\\West Side Story (1961).mkv",
        "audio_amount": 2,
        "audio_summary": "Surround;eng;2;A_DTS;6:default\nStereo;eng;3;A_AAC;2",
        "sub_amount": 2,
        "sub_summary": "eng;4:default\ndut;5",
    }
]
header = [
    "name",
    "year",
    "duration",
    "display_width",
    "display_height",
    "codec_id",
    "location",
    "audio_amount",
    "audio_summary",
    "sub_amount",
    "sub_summary",
]

summaries = {"audio_amount": "audio_summary", "sub_amount": "sub_summary"}

print(
    template.render(
        query_results=query_results,
        header=header,
        summaries=summaries,
        summaries_values=summaries.values(),
    )
)

