// MIT License

// Copyright (c) 2023 Andreas Kröpelin

// Permission is hereby granted, free of charge, to any person obtaining a copy
// of this software and associated documentation files (the "Software"), to deal
// in the Software without restriction, including without limitation the rights
// to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
// copies of the Software, and to permit persons to whom the Software is
// furnished to do so, subject to the following conditions:

// The above copyright notice and this permission notice shall be included in all
// copies or substantial portions of the Software.

// THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
// IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
// FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
// AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
// LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
// OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
// SOFTWARE.

// adapted from: https://github.com/andreasKroepelin/typst-slides/blob/main/themes/bipartite.typ

// This theme is inspired by https://slidesgo.com/theme/modern-annual-report

#let bipartite-theme() = data => {

  let my-dark = rgb("#041E42")  // FAU Dark
  let my-bright = rgb("#EEF2F4")
  let my-accent = rgb("#FC9278")

  let title-slide(slide-info, bodies) = {
    if bodies.len() != 0 {
        panic("title slide of bipartite theme does not support any bodies")
    }

    block(
      width: 100%, height: 60%, outset: 0em, inset: 0em, breakable: false,
      stroke: none, spacing: 0em, fill: my-bright,
      align(center + horizon, text(size: 1.7em, fill: my-dark, data.title))
    )
    block(
      width: 100%, height: 40%, outset: 0em, inset: 0em, breakable: false,
      stroke: none, spacing: 0em, fill: my-dark,
      align(center + horizon, text(fill: my-bright)[
        #text(size: 1.2em, data.subtitle)
        // #v(.0em)

        #text(size: .9em)[ #data.authors.join(", ") #h(1em) #sym.dot.c #h(1em) #data.date ]
      ])
    )
    place(
      center + horizon, dy: 10%,
      rect(width: 6em, height: .5em, radius: .25em, fill: my-accent)
    )
  }

  let displayed-title(slide-info) = if "title" in slide-info {
    heading(level: 2, text(fill: my-bright, slide-info.title))
  } else {
    []
  }

  let west(slide-info, bodies) = {
    if bodies.len() != 1 {
      panic("default variant of bipartite theme only supports one body per slide")
    }
    let body = bodies.first()

    box(
      width: 30%, height: 100%, outset: 0em, inset: (x: 1em), baseline: 0em,
      stroke: none, fill: my-dark,
      align( left + horizon, displayed-title(slide-info) )
    )
    box(
      width: 70%, height: 100%, outset: 0em, inset: (x: 1em), baseline: 0em,
      stroke: none, fill: my-bright,
      align(left + horizon, text(fill: my-dark, body))
    )
  }

  let east(slide-info, bodies) = {
    if bodies.len() != 1 {
      panic("east variant of bipartite theme only supports one body per slide")
    }
    let body = bodies.first()

    box(
      width: 70%, height: 100%, outset: 0em, inset: (x: 1em), baseline: 0em,
      stroke: none, fill: my-bright,
      align(right + horizon, text(fill: my-dark, body))
    )
    box(
      width: 30%, height: 100%, outset: 0em, inset: (x: 1em), baseline: 0em,
      stroke: none, fill: my-dark,
      align( right + horizon, displayed-title(slide-info) )
    )
  }

  let center-split(slide-info, bodies) = {
    if bodies.len() != 2 {
      panic("center split variant of bipartite theme only supports two bodies per slide")
    }
    let body-left = bodies.first()
    let body-right = bodies.last()

    box(
      width: 50%, height: 100%, outset: 0em, inset: (x: 1em), baseline: 0em,
      stroke: none, fill: my-bright,
      align(right + horizon, text(fill: my-dark, body-left))
    )
    box(
      width: 50%, height: 100%, outset: 0em, inset: (x: 1em), baseline: 0em,
      stroke: none, fill: my-dark,
      align(left + horizon, text(fill: my-bright, body-right))
    )
  }

    let blank(slide-info, bodies) = {
    if bodies.len() != 1 {
      panic("blank variant of bipartite theme only supports one body per slide")
    }
    let body = bodies.first()

    box(
      width: 100%, height: 100%, outset: 0em, inset: (x: 1em), baseline: 0em,
      stroke: none, fill: my-bright,
      align(right + horizon, text(fill: my-dark, body))
    )
  }

  (
    "title slide": title-slide,
    "default": west,
    "east": east,
    "center split": center-split,
    "blank": blank,
    "image": image,
  )
}
