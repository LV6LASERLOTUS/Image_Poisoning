import os
import sys
from PIL import Image
from torch.utils.data import Dataset

class FaceDataset(Dataset):
    
    def __init__(self, root_path:str, transform=None):
        
        self.root_path=root_path
        
        self.transform = transform

        # create a dictionary labeling female_faces,male_faces,object to a number
        self.img_labels:dict[str:int]={dir_name:i for i,dir_name in enumerate(sorted(os.listdir(root_path)))}

        self.samples:list[tuple(str,int)] = []

        # Retrieving each image and saving it as a tuple to samples
        for folder_name in os.listdir(self.root_path):
            folder_path:str = os.path.join(self.root_path,folder_name)         
            for img in os.listdir(folder_path):
                try:
                    self.samples.append(( os.path.join(folder_path,img), self.img_labels[folder_name]))
                except Exception as e:
                    print(f'{e}')

    def __len__(self):
        return len(self.samples)
        
    def __getitem__(self,index):
        
        img_path, label = self.samples[index]
        img = Image.open(img_path).convert('RGB')

        if self.transform:
            img = self.transform(img)

        return (img, label)