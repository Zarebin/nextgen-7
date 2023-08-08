from torch.utils.data import Dataset
import pandas as pd


class TextDataset(Dataset):
    def __init__(self, list_of_csv_files):
        df = pd.concat((pd.read_csv(filename) for filename in list_of_csv_files))
        self.df = df.dropna()

        self.main_text = df['main_text'].tolist()
        self.og = df['og_description'].tolist()

    def __len__(self):
        return len(self.df)

    def __getitem__(self, idx):
        main_text = self.main_text[idx]
        description = self.og[idx]

        start_index = main_text.find(description)
        end_index = start_index + len(description) - 1

        return main_text, (start_index, end_index)
