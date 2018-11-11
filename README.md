# ShitpostBot2018
## Introduction
This a follow up to [ShitpostBot2000](https://github.com/JSeam2/ShitpostBot2000). With updated models and interface. The data used was from facebook.

## To make your own shitpost bot
1. You can go to facebook settings to download your post information. Most of the text data is concentrated under Posts, Comments, Messages, and Groups. We will use these data to train.

2. Once ready download the data from facebook.

3. Clone this repo. Extract the .zip file into the root folder of this repo. You will need to modify the following lines in the preprocess.py file

```
AUTHOR = 'YOUR FACEBOOK NAME'
ROOT = './facebook-yourname'
```

4. Run the training scripts to generate the model. *TODO* 

5. Upload the model to aws lambda *TODO* 

6. Upload the frontend to a static host *TODO*

7. Serve
