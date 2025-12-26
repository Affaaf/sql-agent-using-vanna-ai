from vanna.tools import RunSqlTool
from vanna.integrations.mysql import MySQLRunner
import os

def create_db_tool():
    return RunSqlTool(
        sql_runner=MySQLRunner(
            host=os.getenv("MYSQL_HOST"),
            port=int(os.getenv("MYSQL_PORT")),
            user=os.getenv("MYSQL_USER"),
            password=os.getenv("MYSQL_PASSWORD"),
            database=os.getenv("MYSQL_DB"),
        ),
    )
