import sqlite3 as sq
from uuid import uuid4


async def db_start():
    global db, cur
    db = sq.connect('soff_bot.db')
    cur = db.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS section(section_id TEXT PRIMARY KEY, name TEXT NOT NULL)")

    cur.execute("CREATE TABLE IF NOT EXISTS lesson("
                "lesson_id TEXT PRIMARY KEY, "
                "name TEXT NOT NULL, "
                "video TEXT NOT NULL,"
                "handout TEXT NOT NULL,"
                "homework TEXT,"
                "section_id TEXT NOT NULL, FOREIGN KEY (section_id) REFERENCES section(section_id))")
    db.commit()


async def create_section(name):
    section = cur.execute("SELECT 1 FROM section WHERE name = '{key}'".format(key=name)).fetchone()
    if not section:
        cur.execute("INSERT INTO section VALUES(?, ?)", (str(uuid4()), name))
        db.commit()


def create_lesson(name, section_id):
    lesson = cur.execute("SELECT 1 FROM lesson WHERE name = '{key}'".format(key=name)).fetchone()
    if not lesson:
        cur.execute("INSERT INTO lesson VALUES(?, ?, ?)", (None, name, section_id))
        db.commit()


def get_all_sections():
    cur.execute("INSERT INTO section VALUES(?, ?)", (str(uuid4()), 'test 1'))
    cur.execute("INSERT INTO section VALUES(?, ?)", (str(uuid4()), 'test 2'))
    sections = cur.execute("SELECT section_id, name FROM section").fetchall()
    return sections


def get_all_lessons_by_sec(section_id):
    cur.execute("INSERT INTO lesson VALUES(?, ?, ?, ?, ?, ?)", (str(uuid4()), 'test 1', 'test 1', 'test 1', 'test 1', section_id))
    lessons = cur.execute("SELECT lesson_id, name FROM lesson WHERE section_id = '{key}'".format(key=section_id)).fetchall()
    return lessons


def get_section(section_id):
    section = cur.execute("SELECT name FROM section WHERE section_id = '{key}'".format(key=section_id)).fetchone()
    if section:
        return section[0]


def get_lesson(lesson_id):
    lesson = cur.execute("SELECT * FROM lesson WHERE lesson_id = '{key}'".format(key=lesson_id)).fetchone()
    if lesson:
        return lesson


def edit_lesson(name, section_id):
    cur.execute("UPDATE lesson SET section_id = '{}' WHERE name == '{}'".format(section_id, name))
    db.commit()


def edit_section(name, section_id):
    section = cur.execute("SELECT 1 FROM section WHERE name = '{key}'".format(key=name)).fetchone()
    if section:
        cur.execute("UPDATE section SET name = '{}' WHERE section_id == '{}'".format(name, section_id))
        db.commit()


def delete_lesson(name):
    lesson = cur.execute("SELECT 1 FROM lesson WHERE name = '{key}'".format(key=name)).fetchone()
    if lesson:
        cur.execute("DELETE FROM lesson WHERE name = '{}'".format(name))
        db.commit()


def delete_section(name):
    section = cur.execute("SELECT 1 FROM section WHERE name = '{key}'".format(key=name)).fetchone()
    if section:
        cur.execute("DELETE FROM section WHERE name = '{}'".format(name))
        db.commit()

