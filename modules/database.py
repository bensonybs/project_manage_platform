import pandas as pd
import os
from pymongo import MongoClient
from datetime import datetime

import pymongo


class MongoDB():
    """
    - Mongo Server URI需要先在環境變數中設定，再由os.environ引用
    - 考慮應該不常會有切換database的狀況，將database名稱寫入 DATABASE_NAME
    """
    def __init__(self, uri_variable, database_name):
        self.MONGO_SERVER = os.environ[uri_variable] # Mongo Database URI, save in os.environ variable
        self.DATABASE_NAME = database_name
        # Connect to local server
        self.client = MongoClient(self.MONGO_SERVER)
        self.db = self.client[self.DATABASE_NAME]
        self.sort_direction = {'asc': pymongo.ASCENDING, 'desc': pymongo.DESCENDING}

    def insertDocuments(self,
                        documents: list[dict],
                        to_collection: str,
                        drop_existing_database: bool = False,
                        drop_existing_collections: bool = False):
        """
        - 新增資料至MongoDB
        - 參數   
        documents: 要新增的資料(資料型態為dictionary的list，結構類似JSON，由key: value 組成)，可插入單筆或多筆;
        to_collection: 要新增資料的目標collection名稱，為string;
        drop_existing_database: 新增資料時是否要刪除現存database，重新建立一個一樣名字的資料庫(請小心使用)，預設為false;
        drop_existing_collections: 新增資料時是否要刪除現存collection，重新建立一個一樣名字的集合(請小心使用)，預設為false; 
        """
        # Connect to local server
        client = MongoClient(
            self.MONGO_SERVER
        )  # Mongo Database URI, save in os.environ variable
        # Create database
        if drop_existing_database:
            self.client.drop_database(self.DATABASE_NAME)
            print(
                f'* Drop existing database, {{name: \'{self.DATABASE_NAME}\'}}'
            )
        self.db = self.client[self.DATABASE_NAME]
        # Create Collections (table)
        collection = self.db[to_collection]
        if drop_existing_collections:
            self.db.drop_collection(to_collection)
            print(f'* Drop old collection: {to_collection}')
        # Insert documents (rows) into the database's collection (table)
        collection.insert_many(documents)

    def getDocuments(self,
                     from_collection: str,
                     query: dict = None,
                     sorting: dict = None):
        """
        - 從指定集合取得符合條件的資料
        - 參數
        from_collection: 要查詢資料的目標collection名稱，為string;
        query: 查詢條件, 為dictionary, 預設為None, 可回傳該集合內所有資料;
        sorting: 由 {field: direction} 組成的 dictionary, field: 要排序的欄位, direction: 要排序的方向, asc(升冪), desc(降冪);
        """
        collection = self.db[from_collection]
        result = collection.find(query)
        if sorting:
            field = list(sorting.keys())[0]
            direction = self.sort_direction[list(sorting.values())[0]]
            result = result.sort(field, direction)
        return list(result)

    def updateDocuments(
        self,
        from_collection: str,
        query: dict,
        update_value: dict
    ):
        """
        - 從指定集合取得符合條件的資料並進行更新
        - 參數
        from_collection: 要查詢資料的目標collection名稱, 為string;
        query: 查詢條件, 為dictionary;
        update_value: 要更新的欄位及更新值，為dictionary, {filed: update_value}
        """
        collection = self.db[from_collection]
        updateRows = collection.update_many(filter=query, update={'$set': update_value}).raw_result['n'] # update_many() Return a dictionary: raw_result {'n': update rows, 'ok': 1.0}
        if updateRows == 0:
            raise Exception('No matching query to be updated.')
        result = f'Update {updateRows} rows from {self.DATABASE_NAME}.{from_collection}' 
        print(result)
        return None

    def deleteDocuments(
        self,
        from_collection: str,
        query: dict,
    ):
        """
        - 從指定集合取得符合條件的資料並進行刪除，若沒有找到要刪除的資料即會報錯
        - 參數
        from_collection: 要查詢資料的目標collection名稱，為string;
        query: 查詢條件, 為dictionary;
        """
        collection = self.db[from_collection]
        deleteRows = collection.delete_many(filter=query).raw_result['n'] # delete_many() Return a dictionary: raw_result {'n': delete rows, 'ok': 1.0}
        if deleteRows == 0:
            raise Exception('No matching query to be deleted.')
        result = f'Delete {deleteRows} rows from {self.DATABASE_NAME}.{from_collection}' 
        print(result)
        return None

EXCEL_DATA_PATH = './data/database.xlsx'


def getDataFrameFromExcel(sheet_name: str):
    # 取得填報碳排專案主頁資料
    df = pd.read_excel(EXCEL_DATA_PATH, sheet_name)
    return df

# Exports 
mongoDatabase = MongoDB('MONGODB_RPA_SERVER', 'decarbon_platform')
projects = getDataFrameFromExcel('projects')
project_details = getDataFrameFromExcel('project_details')
production_emission = getDataFrameFromExcel('raw_production_emission')

if __name__ == '__main__':
    # for i in range(3):
    #     mongoDatabase.insertDocuments( [{'title' : '測試', 'content': '隨意'+str(i), 'date': datetime.now()}], 'announcements')
    # mongoDatabase.updateDocuments('announcements', {'title': '測試'}, {'title' : '測試Update', 'content': '測試值'})
    # mongoDatabase.deleteDocuments('announcements', {'title': '測試Update'})
    # df = mongoDatabase.getDocuments('announcements', {'title': '測試'}, sorting={'date': 'desc'})
    # print(df[0])
    pass
