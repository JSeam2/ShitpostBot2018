# ShitpostBot2018
# Introduction
This a follow up to [ShitpostBot2017](https://github.com/JSeam2/ShitpostBot2017). With updated models and interface. The data used was from facebook.
The goal of the ShitpostBot is to immortalize my social media presence and shitposts using AI. Should I die, there's at least some digital representation of what I once was. The previous model was dumb, so I had to improve it. I guess I would improve the model continuously given advances in NLP techniques.

# Models Used and Explanations
## Markov Chain Generator
TODO

## LSTM RNN Generator
TODO

## TextGAN Generator
TODO

# Deployed At
[www.jseambot.com](www.jseambot.com)

# Literature Referenced
For this incarnation of the shitpost bot, I've decided to look additionally into Generative Adversarial Nets (GAN). As GANs only work well for continuous real values, dealing with discrete values like words are problematic. As such I've referenced the following literature which provided very useful insights.

1. [SeqGAN: Sequence Generative Adversarial Nets with Policy Gradient by Lantao Yu, Weinan Zhang, Jun Wang, Yong yu](https://arxiv.org/pdf/1609.05473.pdf)
2. [Generating Text via Adversarial Training by Yizhe Zhang, Zhe Gan, Lawrence Carin](https://zhegan27.github.io/Papers/textGAN_nips2016_workshop.pdf)
3. [Adversarial Feature Matching for Text Generation by Yizhe Zhang, Zhe Gan, Kai Fan, Zhi Chen, Ricardo Henao, Dinghan Shen, Lawrence Carin](https://arxiv.org/pdf/1706.03850.pdf)
