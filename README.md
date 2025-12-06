![Python Version](https://img.shields.io/badge/Python-%3E%3D3.10-blue) ![PyTorch Version](https://img.shields.io/badge/PyTorch-2.1-orange)


# Comparison of IVT,SVD watermarking vs CMUA/FOUND on jpg and png

#  Description:

Nowadays with the growth of AI, our personal data is becoming more and more prone to use as training data and for production of deepfakes, both without our consent. Therefore, to counter such attacks a watermarking method aimed toward the neural network models used for such nonconsensual data scraping is needed, but at the same time this watermarking method should not degrade image quality itself. Therefore, in this project, we aim to test out two broad categories of watermarking techniques to protect images against training and deepfakes by AI. 

- [Feature Extraction Matters More](https://arxiv.org/pdf/2303.00200)
-  [Secure and flexible image watermarking using IWT, SVD, and chaos models for robustness and imperceptibility](https://www.nature.com/articles/s41598-025-91876-2)

# 📚 Contents

-[ Getting Started](#-Getting-Started)
- [Implementation Explanation](#-Implementation-Explanation)
  - [Model Choice](#Model-Choice)
  - [Found Watermarking](#Found-Watermarking)

# 🚀 Getting Started


# 🧩 Implementation Explanation

### Model Choice
For this project, we selected the VGG13 convolutional neural network architecture proposed by [Simonyan and Zisserman (2004)](https://arxiv.org/abs/1409.1556) as the backbone model for evaluating watermarking and attacks on model usage. Our implementation is built entirely from scratch, with a slight modification to the original design by adding BatchNorm2d layers to promote smoother gradient flow and a more stable convergence during training.

<img width="640" height="354" alt="Image" src="https://github.com/user-attachments/assets/6c3b8d42-74d0-44af-8333-20a4612da7c1" />

### Found-Watermarking

The implementation of Found is split into mainly three parts

1) Extracting base image feature vector from the model
2) Adding Gaussian Noise to image 
3) Extracting feature vector of watermark image
4) Comptuing Mse of watermark feature vector to the base image feature vector
