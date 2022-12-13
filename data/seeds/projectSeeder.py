"""載入預設專案資料至Mongo資料庫"""
import os
from pprint import pprint
import pandas as pd
from pymongo import MongoClient
# Import user-defined module in project_manage_platform/modules
import sys
sys.path.append('D:/04_桌上型電腦D槽/01_Git_Repository/project_manage_platform/modules')

# Create the documents (rows)
"""The data below is needed in other place"""
def getDataFrameFromExcel(sheet_name: str):
    EXCEL_DATA_PATH = './data/database.xlsx'
    # 取得填報碳排專案主頁資料
    df = pd.read_excel(EXCEL_DATA_PATH, sheet_name)
    return df
projects = getDataFrameFromExcel('projects')
project_details = getDataFrameFromExcel('project_details')
production_emission = getDataFrameFromExcel('raw_production_emission')

def createSeedData(dropExistingDataBase: bool = False, dropExistingCollections: bool = False):
    """dropExistingDataBase: 刪除現有同名資料庫，預設為False, dropExistingCollections: 刪除現有同名collection，預設為False"""
    # Connect to local server
    client = MongoClient(os.environ['MONGODB_RPA_SERVER']) # Mongo Database URI, save in os.environ variable

    # Create database 
    DATABASE_NAME = 'decarbon_platform'
    if dropExistingDataBase:
        client.drop_database(DATABASE_NAME)
        print(f'* Drop existing database, {{name: \'{DATABASE_NAME}\'}}')
    db = client[DATABASE_NAME]

    # Create Collections (table)
    COLLECTION_NAME1 = 'projects'
    COLLECTION_NAME2 = 'project_details'
    COLLECTION_NAME3 = 'raw_production_emission'
    collections = [db[COLLECTION_NAME1], db[COLLECTION_NAME2], db[COLLECTION_NAME3]]
    if dropExistingCollections:
        for collection in collections:
            db.drop_collection(collection)
            print(f'* Drop old collection: {collection.name}')

    # Insert documents (rows) into the database's collection (table)
    collections[0].insert_many(projects.to_dict(orient='records'))
    collections[1].insert_many(project_details.to_dict(orient='records'))
    collections[2].insert_many(production_emission.to_dict(orient='records'))

    # View the documents
    testing = [collection.find_one() for collection in collections]
    print('* Insert seed data successfully, show one document in each collection below: ')
    pprint(testing)

if __name__ == '__main__':
  createSeedData(dropExistingCollections=True)