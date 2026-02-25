from app.clients.appwrite_client import tablesDB
from app.core.config import config
from appwrite.query import Query

def get_pair(pair_id: str):
    try:
        rows = tablesDB.list_rows(
            database_id=config.APPWRITE_DATABASE_ID,
            table_id=config.APPWRITE_PAIR_COLLECTION_ID,
            queries=[
                Query.equal("$id", pair_id),
                Query.equal("isComplete", True),
                Query.equal("status", "active"),
            ]
        )
        if rows['total'] == 0:
            return None
        return rows['rows'][0]
    except Exception as e:
        print("Error fetching pair:", e)
        return None