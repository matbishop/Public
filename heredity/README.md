# Heredity

Requirements: [https://cs50.harvard.edu/ai/2020/projects/2/heredity/#example-joint-probability](https://cs50.harvard.edu/ai/2020/projects/2/heredity/#example-joint-probability)

> The project implements AI to help with making inference about a population, where inference will be made on the probability distribution for each person's genes in the population, as well as the probability distribution for whether a person will exhibit the trait in question.

This is done with the help of a Bayesian Network. The trait in question regards a person having hearing loss, which is dependant (in some cases) on the amount of GJB2 genes the person has. This is dependant on the amount of GJB2 genes the persons parents have, subject also to a chance of the gene mutating.

## Inference by Enumeration

![Inference formula](formula.png)

In this formula, `X` is the query variable, `e` the observed evidence, `y` is all values of hidden variables and `α` is a normalising factor. The formula allows us to express a conditional probabilty as the sum of unconditional, joint probabilities.