#import "../slides_template/slides.typ": *
#import "../slides_template/bipartite.typ": *

#show: slides.with(
    authors: ("Kilian Wenker"), short-authors: "KW",
    title: "Weather Conditions and Music Preferences", subtitle: "Advanced Methods of Software Engineering",
    date: "2023-06-28",
    theme: bipartite-theme(),
)

#slide(theme-variant: "title slide")

#slide(title: "Introduction")[
  Briefly introduces the topic and its significance. \
  Highlights the data science question: Does weather influence music preferences? \

  #lorem(20)
]

#slide(title: "Data Sources")[
  *1. Weather data*
    - Daily Weather Data for Germany
    - Source: Deutscher Wetterdienst (DWD)
    - Format: _CSV / KL2000_

  *2. Music data*
    - Daily Spotify Charts for Germany
    - Source: _Kaggle_
    - Format: _CSV_
    #pad(y: -5pt, [])
    - Song's Audio Features
    - Source: _Spotify_
    - Format: _JSON_
]

#slide(title: "Preprocessing")[
  Explains the steps taken to obtain and preprocess the data.
]

#slide(title: "Correlations")[
  Showcases Correlations in the data.
]

#slide(title: "Random Forest Regressor")[
  Discusses the ML model used for prediction.
  Highlights the model's performance evaluation.
  Shows Barchart learings and excerpt example of a tree.
]

#slide(title: "Song Recommendation")[
  Explains how to use the RFR model.
  Showcases a Song Recommendation.
]

#slide(title: "Conclusion")[
  Summarizes the main findings and answers DS question.
  Mentions limitations and areas for further research.
]

#slide(title: "Q&A")[
  Allocates time for questions and open the floor for discussion.
  Engages with the audience and address any queries or feedback.
]