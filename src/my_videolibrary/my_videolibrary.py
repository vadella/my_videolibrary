def _summarize_tracks(tracks):
    return dict(amount=len(tracks), summary="\n".join(map(str, tracks)))


class Movie:
    def __init__(self, properties):
        self._properties = properties.copy()
        self._audiotracks = [
            AudioTrack(track) for track in properties.pop("audio_tracks", [])
        ]
        self._subtitle_tracks = [
            SubtitleTrack(track)
            for track in properties.pop("subtitle_tracks", [])
        ]

    def __getitem__(self, key):
        return self._properties[key]

    def get(self, key, default=None):
        self._properties.get(key, default)

    @property
    def summary_general(self):
        items = (
            "name",
            "year",
            "duration",
            "display_width",
            "display_height",
            "codec_id",
            "location",
        )
        return {item: self[item] for item in items}

    @property
    def summary_audio(self):
        return _summarize_tracks(self._audiotracks)

    @property
    def summary_subtitle(self):
        return _summarize_tracks(self._subtitle_tracks)

    @property
    def summary_complete(self):
        return dict(
            **self.summary_general,
            **{
                f"audio_{key}": value
                for key, value in self.summary_audio.items()
            },
            **{
                f"sub_{key}": value for key, value in self.summary_subtitle.items()
            },
        )

    def __repr__(self):
        properties = dict(
            **self._properties,
            audiotracks=self._audiotracks,
            subtitletracks=self._subtitle_tracks,
        )
        return f"{type(self).__name__}({properties})"


class Track:
    _class_fields: tuple
    _suffixes: dict = {}

    def __init__(self, properties):
        self._properties = properties

    @property
    def _fields(self):
        return [
            f"{self._properties.get(field, '')}{type(self)._suffixes.get(field,'')}"
            for field in self._class_fields
        ]

    def __str__(self):
        return (
            ";".join(self._fields) + (":default" if self._properties["default"] else "")
        )

    def __repr__(self):
        return f"{type(self).__name__}(properties={self._properties.copy()})"


class AudioTrack(Track):
    _class_fields = ("name", "language", "number", "codec_id", "channels")
    _suffixes = {"channels": "ch"}


class SubtitleTrack(Track):
    _class_fields = ("language", "number")