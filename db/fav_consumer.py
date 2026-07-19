import pika
import json
import bcrypt
import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))

mydb = mysql.connector.connect(
    host=os.getenv('DB_HOST'),
    port=int(os.getenv('DB_PORT')),
    database=os.getenv('DB_NAME'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASS'),
    ssl_disabled=True
)

def save_favorite(user_id, list_name, item_id, item_type):
    if not user_id or not list_name or not item_id or not item_type:
        return {'success': False, 'message': 'User ID, list name, item ID, and item type are required'}

    cursor = None
    try:
        cursor = mydb.cursor()
        sql = "INSERT INTO favorites (user_id, list_name, item_id, item_type) VALUES (%s, %s, %s, %s)"
        val = (user_id, list_name, item_id, item_type)
        cursor.execute(sql, val)
        mydb.commit()
        return {'success': True, 'message': 'Favorite saved successfully'}
    except mysql.connector.errors.IntegrityError:
        mydb.rollback()
        return {'success': False, 'message': 'Favorite already exists'}
    except Exception:
        mydb.rollback()
        return {'success': False, 'message': 'Failed to save favorite'}
    finally:
        if cursor:
            cursor.close()

def get_favorites(user_id):
    if not user_id:
        return {'success': False, 'message': 'User ID is required'}

    cursor = None
    try:
        cursor = mydb.cursor()
        sql = "SELECT * FROM favorites WHERE user_id = %s"
        val = (user_id,)
        cursor.execute(sql, val)
        rows = cursor.fetchall()
        return {'success': True, 'data': rows, 'message': 'Favorites retrieved successfully'}
    except Exception:
        return {'success': False, 'message': 'Failed to retrieve favorites'}
    finally:
        if cursor:
            cursor.close()

def rename_list(user_id, old_name, new_name):
    if not user_id or not old_name or not new_name:
        return {'success': False, 'message': 'User ID, old name, and new name are required'}

    cursor = None
    try:
        cursor = mydb.cursor()
        sql = "UPDATE favorites SET list_name = %s WHERE user_id = %s AND list_name = %s"
        val = (new_name, user_id, old_name)
        cursor.execute(sql, val)
        mydb.commit()
        return {'success': True, 'message': 'List renamed successfully'}
    except Exception:
        mydb.rollback()
        return {'success': False, 'message': 'Rename failed'}
    finally:
        if cursor:
            cursor.close()

def filter_favorites(user_id, item_type):
    if not user_id or not item_type:
        return {'success': False, 'message': 'User ID and item type are required'}

    cursor = None
    try:
        cursor = mydb.cursor()
        sql = "SELECT * FROM favorites WHERE user_id = %s AND item_type = %s"
        val = (user_id, item_type)
        cursor.execute(sql, val)
        rows = cursor.fetchall()
        return {'success': True, 'data': rows, 'message': 'Favorites filtered successfully'}
    except Exception:
        return {'success': False, 'message': 'Failed to filter favorites'}
    finally:
        if cursor:
            cursor.close()

def remove_favorite(user_id, item_id, item_type):
    if not user_id or not item_id or not item_type:
        return {'success': False, 'message': 'User ID, item ID, and item type are required'}

    cursor = None
    try:
        cursor = mydb.cursor()
        sql = "DELETE FROM favorites WHERE user_id = %s AND item_id = %s AND item_type = %s"
        val = (user_id, item_id, item_type)
        cursor.execute(sql, val)
        mydb.commit()
        return {'success': True, 'message': 'Favorite removed successfully'}
    except Exception:
        mydb.rollback()
        return {'success': False, 'message': 'Failed to remove favorite'}
    finally:
        if cursor:
            cursor.close()