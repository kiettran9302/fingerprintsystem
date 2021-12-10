import sqlite3 as sql
import json

class DB():
    def __init__(self, name):
        self.name = name
        self.conn = None
        self.connect()
    
    def _json_serialize_result(self, result):
        return [dict(row) for row in result]
    
    def connect(self):
        self.conn = sql.connect(self.name, check_same_thread=False)
        
    def close(self):
        self.conn.close()
    
    def retrieve_account(self, username, pswd):
        self.conn.row_factory = sql.Row
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM WEB_ACCOUNT WHERE WEB_ACCOUNT.usrname = '{}' AND WEB_ACCOUNT.pswd = '{}'".format(username, pswd))
        rows = cur.fetchall()
        return self._json_serialize_result(rows)
    
    def retrieve_student(self, fingerprint_id):
        self.conn.row_factory = sql.Row
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM STUDENT WHERE STUDENT.fingerprint_id = {}".format(fingerprint_id))
        rows = cur.fetchall()
        return self._json_serialize_result(rows)
    
    def retrieve_checkin_status_join_student(self):
        self.conn.row_factory = sql.Row
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM STUDENT JOIN CHECKIN_STATUS WHERE STUDENT.id = CHECKIN_STATUS.STUDENT_id")
        rows = cur.fetchall()
        return self._json_serialize_result(rows)
    
    def update_checkin_status(self, checkin_status, student_id, checkin_date):
        self.conn.row_factory = sql.Row
        cur = self.conn.cursor()
        cur.execute("UPDATE CHECKIN_STATUS SET checkin_status = '{}' WHERE STUDENT_id = {} AND checkin_date = '{}'".format(checkin_status, student_id, checkin_date));
        self.conn.commit()
