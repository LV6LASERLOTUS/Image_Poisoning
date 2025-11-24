import torch
import torch.nn as nn 
from torch import Tensor


class DoubleConv(nn.Module):
    
    """
    A double convolutional Layer with 3x3, ReLU, and optional MaxPooling
    
    includes a foward method to pass argument forward
    
    Attributes:
    
        in_channels (int): The dimensin of the img 
        out_channels (int): The number of classification
        use_pooling (bool): Whether or not to use pooling
    """
    
    def __init__(self, in_channels:int, out_channels:int, use_pooling:bool=True):
        super().__init__()
        self.conv_op=nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=3, padding=1), 
            nn.ReLU(),
            nn.Conv2d(out_channels, out_channels, kernel_size=3, padding=1), 
            nn.ReLU(),
        )
        if use_pooling:
            self.pool = nn.MaxPool2d(kernel_size=2,stride=2)
            
    def forward(self,x:Tensor)->Tensor:

        conv = self.conv_op(x)
        pooling = self.pool(conv)
        
        return pooling

class VGG13(nn.Module):
    
    def __init__(self, in_channels:int,num_channels:int):
        super().__init__()

        # 10 layers of Convolution
        self.block1 = DoubleConv(in_channels,64)
        self.block2 = DoubleConv(64,128)
        self.block3 = DoubleConv(128,256)
        self.block4 = DoubleConv(256,512)
        self.block5 = DoubleConv(512,512)

        # Fully connected layers
        self.fc=nn.Sequential(
            nn.Linear(7*7*512,4096),
            nn.ReLU(),
            nn.Linear(4096,4096),
            nn.ReLU(),
            nn.Linear(4096,num_channels)
        ) 

    def extract_features(self,x)->Tensor:
        
        down1 = self.block1(x)
        down2 = self.block2(down1)
        down3 = self.block3(down2)
        down4 = self.block4(down3)
        down5 = self.block5(down4)
        
        flatten_features = down5.flatten(start_dim=1)

        # Returns a tensor (7*512*512)
        return flatten_features
        
    def forward(self,x):
        
        flatten_x:torch.tensor = self.extract_features(x)
        output = self.fc(flatten_x)
        
        return output
    