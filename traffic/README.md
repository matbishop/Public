# Traffic
*by Matthew Bishop*

Requirements: [https://cs50.harvard.edu/ai/2020/projects/5/traffic/](https://cs50.harvard.edu/ai/2020/projects/5/traffic/)  
Demo: [https://youtu.be/qQmKG7mfEOQ](https://youtu.be/qQmKG7mfEOQ)

In this computer vision project [TensorFlow](https://www.tensorflow.org/) is used to build a neural network to classify road signs based on images of the signs. The [GTSRB](http://benchmark.ini.rub.de/?section=gtsrb&subsection=news) dataset is used which contains thousands of images of 43 different road signs.

A function needs to be implemented to load the data using numpy multidimensional arrays with the help of [OpenCV](https://docs.opencv.org/4.5.2/index.html), as well as resizing the images and adding labels. This function is also platform agnostic.

Another function to create and compile the neural network model is also made with the help of TensorFlow, and detailed below is the process whereby the parameters for the model were determined.


## Model Training Process

Initially, similar parameters to the example provided in the demonstration are used as a starting point - these are as follows:

For the convolutional layer 10 different filters are used with a 3x3 kernel. The input shape is specified in the requirements as the size of the images with 3 channel values to take color into account.

A 2x2 pooling size is used with a max-pooling layer to reduce the size of the input. Afterwards all units are flattened.

Two hidden layers are used: a layer with 40 hidden units and a dropout layer to prevent possible overfitting. An initial value of 0.5 is specified to randomly drop out half of the units from the hidden layer to increase generalisation.

An output layer is specified with a unit for each of the categories the model is trained to learn. A softmax activation is used such that the output can be interpreted with probabilities, and categorical crossentropy is used as the loss function in line with the nature of the classification goal.

Testing these parameters the model initially performs poorly, with accuracy near 5%. Increasing the number of filters to 25 and the units in the hidden layer to 200 lead to a tenfold improvement in accuracy in some cases, and no improvement in other cases. To investigate parameters with less variability in output, dropout is removed. This results in accuracy increasing to levels nearer to 90%. 

Reintroducing a lesser dropout rate of 20% leads to similar accuracy levels but notably reduced loss levels. Adding another hidden layer with identical parameters does not improve the model as currently configured.

Lastly a sigmoid activation function is tried instead of ReLU, which leads to remarkable improvements in accuracy and loss which are calculated as 98% and 0.04 respectively

---

#### Miscellaneous

Please note `requirements.txt` specifies a TensorFlow installation for Macs with Apple silicon. Simply replace the two related lines with `tensorflow`