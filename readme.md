# $\beta$-Variational autoencoders and transformers for reduced-order modelling of fluid flow


## Introduction
The code in this repository features a Python implementation of reduced-order model (ROM) of turbulent flow using $\beta$-variational autoencoders and transformer neural network. More details about the implementation and results from the training are available in ["$\beta$-Variational autoencoders and transformers for reduced-order modelling of fluid flow",Alberto Solera-Rico, Carlos Sanmiguel Vila, M. A. Gómez, Yuning Wang, Abdulrahman Almashjary, Scott T. M. Dawson, Ricardo Vinuesa](https://arxiv.org/abs/2304.03571)

## Data availabilty
1. We share the down-sampled data in [zendo](https://zenodo.org/records/10501216). 

2. We share the pre-trained models of $\beta$-VAE, transformers and LSTM with this repository.

## Training and inference 

+ To train and inference the easy-attention-based transformer, please run: 

        python main.py --model easy


## Structure

+ *data*: Dataset used for the present study 

+ *utils*: Functions

+ *conf*: Configurations for hyper parameters 

+ *nns*: The architecture of neural networks 

+ *res*: Storage of prediction results 

+ *figs*: Storaging figures output 