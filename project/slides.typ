#import "../slides_template/slides.typ": *
#import "../slides_template/bipartite.typ": *

#show: slides.with(
    authors: ("Kilian Wenker"), short-authors: "Short author",
    title: "cool thing", short-title: "Short title", subtitle: "Advanced Methods of Software Engineering",
    date: "2023-06-28",
    theme: bipartite-theme(),
)

#slide(theme-variant: "title slide")

#new-section("section name")

#slide(title: "A longer slide title")[
  #lorem(40)
]

#slide(theme-variant: "east", title: "On the right!")[
  #lorem(40)
]

#slide(theme-variant: "center split")[
  #lorem(40)
][
  #lorem(40)
]
