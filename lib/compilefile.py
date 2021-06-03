import glob
import pandas as pd
import numpy as np

EXCEL_FOLDERPATH = "./data/datafiles/computervision2010_2020/excelversion"
TXT_FOLDERPATH = "./data/datafiles/computervision2010_2020/txtversion"

def compile_excelfiles(folder_path):
    all_data = pd.DataFrame()
    folder_path = folder_path + "/*.xls"
    print(folder_path)
    files = glob.glob(folder_path)
    print("EXCEL")
    print(files)
    print('\n')
    for f in files:
        df = pd.read_excel(f)
        all_data = all_data.append(df, ignore_index=True)
    return all_data


def compile_tabfiles(folder_path):
    txt_data = pd.DataFrame()
    folder_path = folder_path + "/*.txt"
    print(folder_path)
    files = glob.glob(folder_path)
    print("TAB")
    print(files)
    print("\n")
    for f in files:
        print(f)
        df = pd.read_csv(f, sep="\t", lineterminator="\r")
        txt_data = txt_data.append(df)
    return txt_data



if __name__ == "__main__":
    excel_data = compile_excelfiles(EXCEL_FOLDERPATH)
    excel_data.to_excel(EXCEL_FOLDERPATH + "/COMPILED.xlsx", index=False)