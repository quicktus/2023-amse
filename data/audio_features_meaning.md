# A brief summary of spotify's audio features:
- *acousticness:* A measure from 0.0 to 1.0 indicating the confidence of whether a track is acoustic, with 1.0 representing high confidence in its acoustic nature.
- *analysis_url:* A URL providing access to the full audio analysis of a track.
- *danceability:* A number from 0.0 to 1.0 describing how suitable a track is for dancing based on tempo, rhythm stability, beat strength, and regularity.
- *duration_ms:* The duration of the track in milliseconds.
- *energy:* A measure from 0.0 to 1.0 representing the intensity and activity level of a track, with higher values indicating greater energy.
- *track_id:* The unique Spotify ID assigned to a track.
- *instrumentalness:* A measure from 0.0 to 1.0 predicting the likelihood of a track containing no vocal content, with higher values suggesting instrumental tracks.
- *key:* The key in which the track is performed, mapped to standard Pitch Class notation.
- *liveness:* A number from 0.0 to 1.0 indicating the probability of a track being performed live, with higher values suggesting a live recording.
- *loudness:* The overall loudness of a track in decibels (dB), ranging from -60 to 0 dB.
- *mode:* An integer representing the modality (major or minor) of a track, with 1 for major and 0 for minor.
- *speechiness:* A number from 0.0 to 1.0 indicating the presence of spoken words in a track, with higher values suggesting more speech-like recordings.
- *tempo:* The estimated tempo of a track in beats per minute (BPM).
- *valence:* A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track, with higher values indicating more positive emotions.

For a full description of the audio features, see [here](https://developer.spotify.com/documentation/web-api/reference/get-audio-features)