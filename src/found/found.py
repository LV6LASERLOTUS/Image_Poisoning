import torch
import numpy as np


def found(model, img: torch.Tensor, limit: float = 0.07) -> torch.Tensor:
    """ Calculate the watermark to MSE

    This method impements a simplify version of FOUND specifically targetting the 
    VGG13 model. The method adds a Gaussian noise to the base images, and slowly increases
    the noise until it hits the set limit for maximum loss that doesn't affect image visuals.

    Formula:
    
        L_{MSE} = MSE( \sum_{i=1}^{N} E_i(X) , \sum_{i=1}^{N} E_i(Xˆ))

    Args:
    
        model: Custom pytorch model , or using the custom models module
        img: A tensor of shape (Batch , Channel, Height, Width)
        limit: The perturbation limit that doesn't influence visuals
        
    Returns:
        str: The refined response that reached 8/10 score,
            or the last refined response if no acceptable score is met.
    """
    # Check available device
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # Load img to gpu
    img = img.to(device)
    base_features = model.extract_features(img)
    
    # calculate delta from gaussian noie
    x = torch.linspace(-2, 1, 100)
    noises = 1/np.sqrt(2*np.pi) * np.exp(-x**2 / 2)
    
    for noise in noises:
        # Add noise to original image
        watermarked_img = img + noise
        
        watermarked_features = model.extract_features(watermarked_img)
    
        # Calculate MSE
        loss = torch.mean((base_features - watermarked_features)**2)
        
        if loss >= limit:
            return watermarked_img.cpu()

    # If adding noise exceeds limitw
    return img
    