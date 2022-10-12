"""載入預設專案資料至Mongo資料庫"""
import os
from pprint import pprint
import pandas as pd
from pymongo import MongoClient
# Import user-defined module in project_manage_platform/modules
import sys
sys.path.append('D:/04_桌上型電腦D槽/01_Git_Repository/project_manage_platform/modules')
from terminal_color import TerminalColor


# Create the documents (rows)
def getDataFrameFromExcel(sheet_name: str):
    EXCEL_DATA_PATH = './data/database.xlsx'
    # 取得填報碳排專案主頁資料
    df = pd.read_excel(EXCEL_DATA_PATH, sheet_name)
    return df
projects = getDataFrameFromExcel('projects')
project_details = getDataFrameFromExcel('project_details')
production_emission = getDataFrameFromExcel('raw_production_emission')


# Connect to local server
client = MongoClient(os.environ['MONGODB_URI']) # Mongo Database URI, save in os.environ variable

# Create database 
DATABASE_NAME = 'decarbon_platform'
client.drop_database(DATABASE_NAME)
print(f'{TerminalColor.WARNING}Drop existing database, {{name: \'{DATABASE_NAME}\'}}{TerminalColor.ENDC}')
db = client[DATABASE_NAME]


# Create Collections (table)
COLLECTION_NAME1 = 'projects'
COLLECTION_NAME2 = 'project_details'
COLLECTION_NAME3 = 'raw_production_emission'
collections = [db[COLLECTION_NAME1], db[COLLECTION_NAME2], db[COLLECTION_NAME3]]
# Insert documents (rows) into the database's collection (table)
collections[0].insert_many(projects.to_dict(orient='records'))
collections[1].insert_many(project_details.to_dict(orient='records'))
collections[2].insert_many(production_emission.to_dict(orient='records'))

# View the documents
testing = [collection.find_one() for collection in collections]
print('Insert seed data successfully, show one document in each collection below: ')
pprint(testing)




# Convert the Collection (table) date to a pandas DataFrame
# df = pd.DataFrame(list(collection.find()))
# print(df)
# print("----------------------------")
# print(df.iloc[:, 1:])

