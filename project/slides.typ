#import "../slides_template/slides.typ": *
#import "../slides_template/bipartite.typ": *

#show: slides.with(
    authors: ("Kilian Wenker"), short-authors: "KW",
    title: "Weather Conditions and Music Preferences", subtitle: "Advanced Methods of Software Engineering",
    logo: "../media/logo.png",
    date: "2023-06-28",
    theme: bipartite-theme(),
)

#slide(theme-variant: "title slide")

#slide(theme-variant: "blank")[
  #image("../media/song_examples.png")
]

#slide(title: "Data Sources")[
  + *Weather data*
  #pad(x: 30pt, y:-10pt, [
    Daily Weather Data for Germany
    - Source: Deutscher Wetterdienst (DWD)
    - Format: _CSV / KL2000_
  ]) \
  + *Music data*
  #pad(x: 30pt, y:-10pt, [
  Daily Spotify Charts for Germany
  - Source: _Kaggle_
  - Format: _CSV_

  Song's Audio Features
  - Source: _Spotify_
  - Format: _JSON_
  ])
]

#slide(title: "Correlations")[
  Negative correlation between air temperature and song duration.
  #image("../media/duration_vs_air_temperature.png")
]

#slide(title: "Correlations")[
  Positive correlation between cloud coverage and the beats per minute of songs.
  #image("../media/tempo_vs_cloud_coverage.png")
]

#slide(title: "Correlations")[
  Complex relationship between snow height and song's suitability for dancing.
  #image("../media/danceability_vs_snow_height.png")
]

#slide(title: "Random Forest Regressor")[
  The Random Forest Regressor combines predictions from multiple decision trees. This leverages the diversity of the trees to offset their individual errors.
  #image("../media/tree.png")
  #pad(y:-20pt, [#align(center)[#text("Figure: excerpt of one of the trees in the RFR", size: .7cm)]])
]

#slide(title: "Random Forest Regressor")[
  Ranking the features by importance reveals which ones are most informative to the model.
  #image("../media/barchart.png")
]

#slide(title: "RFR usage Example")[
  #image("../media/recommendation_2023-06-26.png")
]

#slide(title: "Q&A")[
  #image("../media/big_science.png")
]