import pandas as pd


def get_excel(path):
    file_path = path
    data = pd.read_excel(file_path)
    rows = data.astype(str).values.tolist() 
    rows = rows[1:]
    return rows



