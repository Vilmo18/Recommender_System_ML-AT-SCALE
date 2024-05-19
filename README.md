# apply_ML_AS
A Recommender System

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![python](https://img.shields.io/badge/Python-14354C?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white)
![NumPy](https://img.shields.io/badge/numpy-%23013243.svg?style=for-the-badge&logo=numpy&logoColor=white)
![Jupyter Notebook](https://img.shields.io/badge/jupyter-%23FA0F00.svg?style=for-the-badge&logo=jupyter&logoColor=white)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ml-at-scale-movies-lens-recommender-system.streamlit.app)



# Project Purpose
The objective of this project is to implement various versions of the Alternating Least Squares (ALS) algorithm for matrix factorization. The three approaches we will explore are:

## 1. ALS with Bias Only

This method optimizes user and item biases to produce robust predictions. It is highly effective for capturing global trends, such as average user ratings and item popularity. However, its simplicity limits its ability to model complex interactions between users and items.

<p align="center">
  <img src="images/file_readme/bias_only_loss_train_page-0001.jpg" alt="train" width="400"/>
  <img src="images/file_readme/bias_only_rsme_train_page-0001.jpg" alt="rmse" width="400"/>
</p>
## 2. ALS with Bias and Latent Vectors

To enhance our model, we will incorporate latent vectors. This allows us to capture more complex relationships between users and items, leading to more personalized and accurate recommendations. By combining biases with latent factors, the model can better understand the unique preferences of users and the specific characteristics of items.
<p align="center">
  <img src="images/file_readme/latent_loss_train_page-0001.jpg" alt="train" width="400"/>
  <img src="images/file_readme/latent_rmse_latent_page-0001.jpg" alt="rmse" width="400"/>
</p>
## 3. ALS with Added Features

To address the cold start problem, where new items or users lack sufficient data for accurate recommendations, we will include item-associated features in our model. By incorporating these features, the model can provide better recommendations even when limited user-item interaction data is available. This approach helps improve the recommendation quality, especially for new or less popular items.

## Visualizing Our Embeddings

Finally, we will visualize our embeddings to better understand the learned representations of users and items. 
<p align="center">
  <img src="images/file_readme/rating.png" alt="Rating" width="400"/>
</p>



# Photos
<p align="center">
  <img src="images/file_readme/info.png" alt="Information" width="400"/>
  <img src="images/file_readme/rating.png" alt="Rating" width="400"/>
</p>

 
# Demo
<p align="center">
  <img src="images/file_readme/prediction.png" alt="Information" width="400"/>
  <img src="images/file_readme/prediction.png" alt="Rating" width="400"/>
</p>

# Social
[![vilmo18](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/Vilmo18)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/yvan-carr%C3%A9-8230442b1/)





