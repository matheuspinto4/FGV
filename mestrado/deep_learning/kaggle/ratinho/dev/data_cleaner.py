import pandas as pd
import os


def concatenate_files(train_annotation_file_path, type):
    for (root, dirs, files) in os.walk(train_annotation_file_path):
        csv_name = root.split(sep="\\")[-1]
        if csv_name == 'train_annotation' or csv_name == 'train_tracking': continue
        
        df_train_annotation = pd.DataFrame() 
        for parquet_file in files:
            parquet_file_path = f"{root}\\{parquet_file}"
            df_parquet = pd.read_parquet(parquet_file_path)
            df_train_annotation = pd.concat([df_train_annotation, df_parquet])

        df_train_annotation.to_parquet(f"cleaned_data\\{type}\\{csv_name}.parquet", index=False)
        print(f"Arquivo {csv_name} gerado com sucesso")




if __name__ == "__main__":
    train_annotation_file_path = 'MABe-mouse-behavior-detection\\train_annotation'
    train_tracking_file_path = 'MABe-mouse-behavior-detection\\train_tracking'
    concatenate_files(train_annotation_file_path, type="annotation")
    concatenate_files(train_tracking_file_path, type="tracking")