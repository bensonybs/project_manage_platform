import pandas as pd

EXCEL_DATA_PATH = './data/database.xlsx'


def getDataFrameFromExcel(sheet_name: str):
    # 取得填報碳排專案主頁資料
    df = pd.read_excel(EXCEL_DATA_PATH, sheet_name)
    return df

projects = getDataFrameFromExcel('projects')
project_details = getDataFrameFromExcel('project_details')
production_emission = getDataFrameFromExcel('raw_production_emission')
if __name__ == '__main__':
    print(production_emission.loc[17])
    