# Help me convert each table in excel files to different csv files in a given directory

import pandas as pd
import os

def excel_to_csv(file_path: str, output_dir: str):
    # Get the file name from the path
    file_name = os.path.basename(file_path)
    # Get the directory name from the path
    dir_name = os.path.dirname(file_path)
    
    df = pd.read_excel(file_path)
    df.to_csv(os.path.join(output_dir, file_name), index=False)


if __name__ == "__main__":
    excel_to_csv("data.xlsx", "DB/CSV")

