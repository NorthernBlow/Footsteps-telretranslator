import psycopg2
from psycopg2 import extras
from psycopg2.extensions import AsIs
from config import DATABASE_URL

# Добавление соответствия идентификаторов
# оригинального и скопированного сообщений
def insert(message):
    connection = psycopg2.connect(DATABASE_URL)
    cursor = connection.cursor()
    try:
        columns = message.keys()
        values = message.values()
        sql_insert = 'insert into BINDING_ID (%s) values %s'
        cursor.execute(sql_insert, (AsIs(','.join(columns)), tuple(values)))
        connection.commit()
    except Exception as e:
        print(e)
    cursor.close()
    connection.close()

# Поиск значения идентификатора скопированного сообщения
# соответствующему идентификатору оригинального сообщения
def find_by_id(message_id):
    try:
        connection = psycopg2.connect(DATABASE_URL)
        cursor = connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute("""
                        SELECT mirror_message_id FROM BINDING_ID
                        WHERE message_id = %s
                        """, (message_id, ))
        rows = cursor.fetchone()
        cursor.close()
        connection.close()
        return rows
    except Exception as e:
        print(e)
