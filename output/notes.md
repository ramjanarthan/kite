### Notes - 24 12 2024

Removing the preprocessing lines (which currently strip out non-alphanumerics) should help improve the recognition of languages, since there's more patterns learned by the model.

Testing the perplexity of the python and c++ models on python validation file <br>
Performance on python validation file<br>
Perplexity of python: 6.14593899640423<br>
Perplexity of c++: 8.967401846037356<br>

Performance on c++ validation file<br>
Perplexity of python: 11.975193045555073<br>
Perplexity of c++: 3.287188133639928<br>

Compared to the previous method of tokenization, it seems that the discriminatory power of these models has worsened (as the scores are closer together now). This method is obviously poor, since it doesn't include the correct adjustments to the smoothing techniques included.

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