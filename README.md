# ShitpostBot2018
# Introduction
This a follow up to [ShitpostBot2000](https://github.com/JSeam2/ShitpostBot2000). With updated models and interface. The data used was from facebook.

# Overview
1. Train model in nlp
2. Upload model to aws lambda to serve the model
3. Present the model in some frontend ui

## To make your own shitpost bot
1. You can go to facebook settings to download your post information. Most of the text data is concentrated under Posts, Comments, Messages, and Groups. We will use these data to train. Do remember to download the files as json and not html.

2. Once ready download the data from facebook.

3. Clone this repo. Extract the .zip file into the /nlp folder of this repo. You will need to modify the following lines in the preprocess.py file

```
AUTHOR = 'YOUR FACEBOOK NAME'
ROOT = './facebook-yourname'
```

4. Run the training scripts to generate the model. *TODO* 

5. Upload the model to aws lambda *TODO* 

6. Upload the frontend to a static host *TODO*

7. Serve
