### Notes - 05 12 2024

Today I updated the code to train, preprocess and build models based on new training data. The first project I used was DeepSpeech repo from Mozilla opensource, since it had a large portion of c++ and python code of high quality (it had > 2K github stars, which as a proxy is at best one of quality, and at worst the number of eyes on this project). <br>

Without modifying the logic of preprocessing, I got the following results for perplexity:<br>

Testing the perplexity of the python and c++ models on python validation file <br>
(base) ➜  kite git:(main) ✗ python custom_model.py <br>
Perplexity of python: 7.346046011249762<br>
Perplexity of c++: 10.286613095191875<br>

Testing the perplexity of the python and c++ models on cpp validation file<br>
(base) ➜  kite git:(main) ✗ python custom_model.py<br>
Perplexity of python: 15.02144925139808<br>
Perplexity of c++: 3.8882049085060895<br>

The models managed to get the predictions right, despite the preprocessing being quite simple and suboptimal. The discriminativeness of the C++ model was impressive, and in comparison to the python model could be due to the larger amount of training data