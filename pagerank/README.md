# PageRank

Requirements: [https://cs50.harvard.edu/ai/2020/projects/2/pagerank/](https://cs50.harvard.edu/ai/2020/projects/2/pagerank/)

> The project implements a PageRank algorithm to rank webpages according to how important they are. In this case, this is determined by how many other pages link to the relevant page, while also taking into account how important the other pages are.

## Logic

Two implementations are done: a random surfer model akin to a Markov Chain, and an iterative algorithm that eventually converges.

![Iterative algorithm formula](formula.png)

A damping factor `d` is used to ensure that all pages in the corpus can be reached.