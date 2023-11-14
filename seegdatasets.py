from pynwb import NWBHDF5IO
import ndx_events  
import torch
from torch.utils.data import Dataset, DataLoader
import os
import pandas as pd

class SEEGDataset(Dataset):
    def __init__(self, file_paths):
        self.seeg_data = []
        self.electrode_positions = []
        for file_path in file_paths:
            self.load_data(file_path)

    def load_data(self, file_path):
        with NWBHDF5IO(file_path, 'r') as io:
            nwbfile = io.read()
            # 提取SEEG数据
            seeg_data = nwbfile.acquisition['ElectricalSeries'].data[:]  
            
            # 首先将数据转换为PyTorch Tensor
            seeg_tensor = torch.from_numpy(seeg_data)

            # 然后使用permute方法重新排列维度
            seeg_tensor = seeg_tensor.permute(1, 0)
            self.seeg_data.append(seeg_tensor)

            # 提取电极位置信息
            electrodes = nwbfile.electrodes.to_dataframe()
            positions = electrodes[['x', 'y', 'z']].values  

            # 将位置信息转换为Tensor
            position_tensor = torch.from_numpy(positions)
            self.electrode_positions.append(position_tensor)


    def __getitem__(self, index):
        return self.seeg_data[index], self.electrode_positions[index]

    def __len__(self):
        return len(self.seeg_data)

# 使用示例
file_paths = ['/home/weichen/projects/shiyin/PE/data/AJILE12/sub-01_ses-3_behavior+ecephys.nwb', '/home/weichen/projects/shiyin/PE/data/AJILE12/sub-02_ses-3_behavior+ecephys.nwb']  
dataset = SEEGDataset(file_paths)

print(len(dataset.seeg_data)) # 被试数
print(len(dataset.electrode_positions)) # 被试数
print(dataset.seeg_data[0].shape) # torch.Size([124, 43200000])
print(dataset.electrode_positions[0].shape) # torch.Size([124, 3])




