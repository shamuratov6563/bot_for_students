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


async def create_lesson(*args):
    lesson = cur.execute('SELECT 1 FROM lesson WHERE name = "{key}"'.format(key=str(args[0]))).fetchone()
    if not lesson:
        cur.execute("INSERT INTO lesson VALUES(?, ?, ?, ?, ?, ?)",
                    (str(uuid4()), args[0], args[1], args[2], args[3], args[4]))
        db.commit()


def get_all_sections():
    sections = cur.execute("SELECT section_id, name FROM section").fetchall()
    return sections


def get_all_sections_name():
    sections = cur.execute("SELECT name FROM section").fetchall()
    return sections


def get_all_lessons_by_sec(section_id):
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


def get_all_lessons_name():
    lessons = cur.execute("SELECT name FROM lesson").fetchall()
    if lessons:
        return lessons
    return None


async def get_lesson_name(lesson_id):
    lesson = cur.execute("SELECT name FROM lesson WHERE lesson_id = '{key}'".format(key=lesson_id)).fetchone()
    if lesson:
        return lesson[0]
    return None


async def edit_lesson_section_id_sql(lesson_id, section_id):
    cur.execute('UPDATE lesson SET section_id = "{}" WHERE lesson_id == "{}"'.format(section_id, lesson_id))
    db.commit()


async def edit_lession_name_sql(name, lesson_id):
    cur.execute('UPDATE lesson SET name = "{}" WHERE lesson_id == "{}"'.format(name, lesson_id))
    db.commit()


async def edit_lesson_video_sql(video, lesson_id):
    cur.execute('UPDATE lesson SET video = "{}" WHERE lesson_id == "{}"'.format(video, lesson_id))
    db.commit()


async def edit_lesson_handout_sql(handout, lesson_id):
    cur.execute('UPDATE lesson SET handout = "{}" WHERE lesson_id == "{}"'.format(handout, lesson_id))
    db.commit()


async def edit_lesson_homework_sql(homework, lesson_id):
    cur.execute('UPDATE lesson SET homework = "{}" WHERE lesson_id == "{}"'.format(homework, lesson_id))
    db.commit()


def edit_section(name, section_id):
    section = cur.execute("SELECT 1 FROM section WHERE name = '{key}'".format(key=name)).fetchone()
    if section:
        cur.execute('UPDATE section SET name = "{}" WHERE section_id == "{}"'.format(name, section_id))
        db.commit()


async def delete_lesson(lesson_id):
    lesson = cur.execute("SELECT 1 FROM lesson WHERE lesson_id = '{key}'".format(key=lesson_id)).fetchone()
    if lesson:
        cur.execute("DELETE FROM lesson WHERE lesson_id = '{}'".format(lesson_id))
        db.commit()


async def delete_section(section_id):
    section = cur.execute("SELECT 1 FROM section WHERE section_id = '{key}'".format(key=section_id)).fetchone()
    if section:
        cur.execute("DELETE FROM section WHERE section_id = '{}'".format(section_id))
        db.commit()
