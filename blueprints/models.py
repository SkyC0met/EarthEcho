from db import get_db_connection

class UnbanRequest:
    def __init__(self, id, user_id, username, reason, status='Pending', timestamp=None):
        self.id = id
        self.user_id = user_id
        self.username = username
        self.reason = reason
        self.status = status
        self.timestamp = timestamp

    @staticmethod
    def get_all():
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM unban_requests")
        requests = cursor.fetchall()
        cursor.close()
        connection.close()
        return requests

    @staticmethod
    def update_status(request_id, status):
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE unban_requests SET status = %s WHERE request_id = %s",
            (status, request_id)
        )
        connection.commit()
        cursor.close()
        connection.close()
