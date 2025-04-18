import sqlite3
from typing import List, Tuple, Optional

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('students.db')
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                roll TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                course TEXT NOT NULL
            )
        ''')
        self.conn.commit()

    def add_student(self, name: str, roll: str, email: str, course: str) -> bool:
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT INTO students (name, roll, email, course)
                VALUES (?, ?, ?, ?)
            ''', (name, roll, email, course))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_all_students(self) -> List[Tuple]:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM students')
        return cursor.fetchall()

    def search_students(self, query: str) -> List[Tuple]:
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM students 
            WHERE name LIKE ? OR roll LIKE ?
        ''', (f'%{query}%', f'%{query}%'))
        return cursor.fetchall()

    def update_student(self, student_id: int, name: str, roll: str, email: str, course: str) -> bool:
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                UPDATE students 
                SET name = ?, roll = ?, email = ?, course = ?
                WHERE id = ?
            ''', (name, roll, email, course, student_id))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def delete_student(self, student_id: int) -> bool:
        try:
            cursor = self.conn.cursor()
            cursor.execute('DELETE FROM students WHERE id = ?', (student_id,))
            self.conn.commit()
            return True
        except:
            return False

    def get_student(self, student_id: int) -> Optional[Tuple]:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM students WHERE id = ?', (student_id,))
        return cursor.fetchone()

    def __del__(self):
        self.conn.close() 