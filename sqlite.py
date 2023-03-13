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
                "section_id TEXT NOT NULL, FOREIGN KEY (section_id) REFERENCES section(section_id))")
    db.commit()


def create_section(name):
    section = cur.execute("SELECT 1 FROM section WHERE name = '{key}'".format(key=name)).fetchone()
    if not section:
        cur.execute("INSERT INTO section VALUES(?, ?)", (None, name))
        db.commit()


def create_lesson(name, section_id):
    lesson = cur.execute("SELECT 1 FROM lesson WHERE name = '{key}'".format(key=name)).fetchone()
    if not lesson:
        cur.execute("INSERT INTO lesson VALUES(?, ?, ?)", (None, name, section_id))
        db.commit()


def get_all_sections():
    cur.execute("INSERT INTO section VALUES(?, ?)", (uuid4(), 'test'))
    sections = cur.execute("SELECT section_id, name FROM section").fetchall()
    return sections


def get_all_lessons(section_id):
    lessons = cur.execute("SELECT name FROM lesson WHERE section_id = '{key}'".format(key=section_id)).fetchall()
    return lessons


def get_section_id(name):
    section = cur.execute("SELECT section_id FROM section WHERE name = '{key}'".format(key=name)).fetchone()
    if section:
        return section[0]


def get_lesson_id(name):
    lesson = cur.execute("SELECT lesson_id FROM lesson WHERE name = '{key}'".format(key=name)).fetchone()
    if lesson:
        return lesson[0]


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

