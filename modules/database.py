import pandas as pd
import os
from pymongo import MongoClient
from datetime import datetime

import pymongo

class MongoDB():
    """
    - 內含四個函式，對MongoDatabase進行CRUD
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

class Excel():
    def __init__(self, excel_path: str):
        self.EXCEL_DATA_PATH = excel_path
        
    def getDataFrameFromSheet(self, sheet_name: str):
        # 取得填報碳排專案主頁資料
        df = pd.read_excel(self.EXCEL_DATA_PATH, sheet_name)
        return df
class SelfDefineData():
    def __init__(self):
        self.companies = ['南亞', '轉投資公司']
        self.division = ['工務部', '化工一部', '化工二部', '化工三部', '塑膠一部', '塑膠二部', '塑膠三部', '電子材料部',
       '聚酯膜部', '纖維部', '文菱科技', '必成', '南中石化', '南亞科技', '南電']
        self.departments = ['工務部其他', '林口公用廠', '配電盤廠', '嘉義公用廠', '嘉義公用廠(新港)', '嘉義機工廠', '樹林公用廠',
       '錦興公用廠', '2EH廠', 'PA廠', '可塑劑廠', '異壬醇廠', 'MA廠', '丁二醇廠', '丙二酚廠',
       '馬來酐廠', '過氧化氫廠', 'EG1', 'EG3', 'EG4', '仁武二廠', '新港一廠', '嘉義三廠',
       '樹林一廠', '門窗一廠', '門窗二廠', '工程塑膠廠', '仁武一廠', '林口廠', '林園廠', '嘉義一廠',
       '嘉義二廠', '嘉義四廠', '玻纖布一廠', '玻纖布二廠', '玻纖布三廠', '玻纖布四廠', '麥寮EPOXY廠',
       '新港CCL一廠', '新港CCL二廠', '新港CCL三廠', '銅箔一廠', '銅箔二廠', '銅箔三廠', '樹三廠',
       '樹林二廠', '製膜一廠', '製膜二廠', '離型膜廠', '公用處', '染整廠', '紡撚一廠', '紡撚三廠',
       '紡撚四廠', '製棉廠', 'XJ', '玻纖絲一、二廠', '玻纖絲一廠', '玻纖絲二廠', 'EG2', '3A',
       '一廠', '二廠', '五廠', '六廠']
        self.project_types = ['政策因素影響', '設備整改汰換', '製程技術改善', '低碳能源轉型', '能源回收利用', '跨廠能源整合', '碳捕捉',
       '其他改善', '智能管理系統', '產量變化影響', '使用再生料取代原生料']
    
# Exports

mongoDatabase = MongoDB(uri_variable='MONGODB_RPA_SERVER', database_name='decarbon_platform')
basicData = SelfDefineData()
excelDataSource = Excel(excel_path='./data/database.xlsx')

if __name__ == '__main__':
    # for i in range(3):
    #     mongoDatabase.insertDocuments( [{'title' : '測試', 'content': '隨意'+str(i), 'date': datetime.now()}], 'announcements')
    # mongoDatabase.updateDocuments('announcements', {'title': '測試'}, {'title' : '測試Update', 'content': '測試值'})
    # mongoDatabase.deleteDocuments('announcements', {'title': '測試Update'})
    # df = mongoDatabase.getDocuments('announcements', {'title': '測試'}, sorting={'date': 'desc'})
    # print(df[0])
    pass
