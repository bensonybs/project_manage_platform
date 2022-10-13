import pandas as pd
import os
from pymongo import MongoClient
from datetime import datetime

import pymongo


def getDocuments(fromCollection: str = 'test',
                 query: dict = None,
                 sorting: dict = None):
    MONGO_SERVER = os.environ['MONGODB_RPA_SERVER']
    DATABASE_NAME = 'decarbon_platform'
    # Connect to local server
    client = MongoClient(
        MONGO_SERVER)  # Mongo Database URI, save in os.environ variable
    # Create database
    db = client[DATABASE_NAME]
    collection = db[fromCollection]
    result = collection.find(query)
    sort_direction = {'asc': pymongo.ASCENDING, 'desc': pymongo.DESCENDING}
    if sorting:
        field = list(sorting.keys())[0]
        direction = sort_direction[list(sorting.values())[0]]
        result = result.sort(field, direction)
    return list(result)


def insertDocuments(documents: list,
                    toCollection: str = 'test',
                    dropExistingDataBase: bool = False,
                    dropExistingCollections: bool = False):
    """
    - 將documents加入database指定collection，可插入單筆或多筆
    - 考慮不常切換database，將database名稱寫入函式 DATABASE_NAME
    - Mongo Server URI則需要先在環境變數中設定，再由os.environ引用
    - 可設定在插入資料時是否要刪除現存data base或collection (dropExistingDataBase, dropExistingCollections)
  """
    MONGO_SERVER = os.environ['MONGODB_RPA_SERVER']
    DATABASE_NAME = 'decarbon_platform'
    # Connect to local server
    client = MongoClient(
        MONGO_SERVER)  # Mongo Database URI, save in os.environ variable
    # Create database
    if dropExistingDataBase:
        client.drop_database(DATABASE_NAME)
        print(f'* Drop existing database, {{name: \'{DATABASE_NAME}\'}}')
    db = client[DATABASE_NAME]
    # Create Collections (table)
    collection = db[toCollection]
    if dropExistingCollections:
        db.drop_collection(toCollection)
        print(f'* Drop old collection: {toCollection}')
    # Insert documents (rows) into the database's collection (table)
    collection.insert_many(documents)


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
