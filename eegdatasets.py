import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np
import os
import mne
import pandas as pd

class EEGDataset(Dataset):
    def __init__(self, base_path, subjects):
        self.eeg_data = []
        self.electrode_positions = []
        self.load_data(base_path, subjects)

    def load_data(self, base_path, subjects):
        for subject in subjects:
            eeg_path = os.path.join(base_path, subject, "eeg", f"{subject}_task-Rest_eeg.set")
            electrode_path = os.path.join(base_path, subject, "eeg", f"{subject}_task-Rest_electrodes.tsv")

            # 加载EEG数据
            raw = mne.io.read_raw_eeglab(eeg_path, preload=True)
            self.eeg_data.append(torch.from_numpy(raw.get_data()))
    

            # 加载电极位置坐标数据
            electrode_df = pd.read_csv(electrode_path, sep='\t')
            positions = electrode_df[['x', 'y', 'z']].values
            self.electrode_positions.append(torch.from_numpy(positions))

    def __getitem__(self, index):
        return self.eeg_data[index], self.electrode_positions[index]

    def __len__(self):
        return len(self.eeg_data)

# 使用示例
base_path = '/home/weichen/projects/shiyin/PE/data/ds004584'
subjects = [f"sub-{i:03d}" for i in range(101, 150)] # 001-100为帕金森患者，101-150为正常人
dataset = EEGDataset(base_path, subjects)

print(len(dataset.eeg_data)) # 被试数
print(len(dataset.electrode_positions)) # 被试数
print(dataset.eeg_data[0].shape) # torch.Size([63, 134450])
print(dataset.electrode_positions[0].shape) # torch.Size([63, 3])


