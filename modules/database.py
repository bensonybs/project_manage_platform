import pandas as pd

EXCEL_DATA_PATH = './data/database.xlsx'


def getFromExcel(sheet_name: str):
    # 取得填報碳排專案主頁資料
    df = pd.read_excel(EXCEL_DATA_PATH, sheet_name, index_col='id')
    return df


projects = getFromExcel('projects')
project_details = getFromExcel('project_details')

if __name__ == '__main__':
    print(projects)