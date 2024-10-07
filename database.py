import mysql.connector
from mysql.connector import Error
from utils import remove_html_tags
import os

blog_connection = mysql.connector.connect(
    host="localhost",
    user=os.environ["DATABASE_USER"],
    password=os.environ["DATABASE_PASSWD"],
    database=os.environ["DATABASE_BLOG"],
)

summary_connection = mysql.connector.connect(
    host="localhost",
    user=os.environ["DATABASE_USER"],
    password=os.environ["DATABASE_PASSWD"],
    database=os.environ["DATABASE_SUMMARY"],
)


def get_wordpress_post_content(post_id):
    try:
        cursor = blog_connection.cursor(dictionary=True)
        query = "SELECT post_content FROM wp_posts WHERE ID = %s AND post_status = 'publish'"
        cursor.execute(query, (post_id,))
        result = cursor.fetchone()

        if result:
            return remove_html_tags(result["post_content"]).replace("\n", "")
        else:
            return None

    except Error as e:
        print(f"Error: {e}")
        return None

    finally:
        cursor.close()


def create_table():
    try:
        create_table_query = """
        CREATE TABLE IF NOT EXISTS SummaryCache (
        ID INT PRIMARY KEY,
        MD5 CHAR(32) NOT NULL,
        content TEXT NOT NULL
        ) ENGINE=InnoDB;
        """

        cursor = summary_connection.cursor(dictionary=True)
        cursor.execute(create_table_query)

    except Error as e:
        print(f"Error: {e}")
        return False

    else:
        summary_connection.commit()

    finally:
        cursor.close()

    return True


def get_content_by_id_and_md5(id_value, md5_value):
    try:
        cursor = summary_connection.cursor()
        query = """
        SELECT content
        FROM SummaryCache
        WHERE ID = %s AND MD5 = %s
        """
        cursor.execute(query, (id_value, md5_value))
        result = cursor.fetchone()

        if result:
            return result[0]
        else:
            return None

    except Error as e:
        print(f"Error: {e}")
        return None

    finally:
        cursor.close()


def update_content_by_id(id_value, md5_value, content_value):
    try:
        cursor = summary_connection.cursor()
        query = """
        INSERT INTO SummaryCache (ID, MD5, content)
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
        MD5 = VALUES(MD5), content = VALUES(content)
        """
        cursor.execute(query, (id_value, md5_value, content_value))

    except Error as e:
        print(f"Error: {e}")
        return None

    else:
        summary_connection.commit()

    finally:
        cursor.close()
