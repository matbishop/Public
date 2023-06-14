# Shopping

Requirements: [https://cs50.harvard.edu/ai/2020/projects/4/shopping/](https://cs50.harvard.edu/ai/2020/projects/4/shopping/)

> The project implements a nearest-neighbour classifier to determine whether a user will make an online purchase based on session information. 

To measure the output of the model, sensitivity (the true positivity rate) is calculated as well as specificity (the true negative rate).

## Functionality

Data is loaded from a CSV file whereafter [scikit-learn](https://pypi.org/project/scikit-learn/) is used to train and fit the model. A nearest neighbour model with `k = 1` is used whereafter the accuracy of the model is measured.