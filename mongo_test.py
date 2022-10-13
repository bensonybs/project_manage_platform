import os
from pprint import pprint
import pandas as pd
from pymongo import MongoClient
from datetime import datetime


def mongoTest(dropExistingDataBase: bool = False,
              dropExistingCollections: bool = False):
    # Create the documents (rows)
    documents = [{
        'title': '碳排減量專案平台公告',
        'content': '管理者可在設定新增公告，公告會顯示於首頁',
        'date': datetime.now()
    }, {
        'title': '碳排減量會議',
        'content': '各位主管 您好: 塑膠群碳排減量報告於7/13(四) 14:00。',
        'date': datetime.now()
    }]

    # Connect to local server
    client = MongoClient(os.environ['MONGODB_RPA_SERVER']
                         )  # Mongo Database URI, save in os.environ variable

    # Create database
    DATABASE_NAME = 'decarbon_platform'
    if dropExistingDataBase:
        client.drop_database(DATABASE_NAME)
        print(f'* Drop existing database, {{name: \'{DATABASE_NAME}\'}}')
    db = client[DATABASE_NAME]

    # Create Collections (table)
    COLLECTION_NAME1 = 'announcements'
    collections = [db[COLLECTION_NAME1]]
    if dropExistingCollections:
        for collection in collections:
            db.drop_collection(collection)
            print(f'* Drop old collection: {collection.name}')

    # Insert documents (rows) into the database's collection (table)
    collections[0].insert_many(documents)

    # View the documents
    testing = [collection.find_one() for collection in collections]
    print(
        '* Insert data successfully, show one document in each collection below: '
    )
    pprint(testing)

    # Convert the Collection (table) date to a pandas DataFrame
    # df = pd.DataFrame(list(collection.find()))
    # print(df)
    # print("----------------------------")
    # print(df.iloc[:, 1:])


if __name__ == '__main__':
    mongoTest(dropExistingCollections=True)
