import os
import sqlite3
import fire
from datetime import datetime
import datetime

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'database.sqlite3')

conn = sqlite3.connect(DEFAULT_PATH)

cur = conn.cursor()

print()
print('######################################################')
print('To add user: python todo.py add_user "USER NAME" "USER EMAIL" "PROJECT ID" ')
print('To add project: python todo.py add_project "PROJECT NAME" "PROJECT DESCRIPTION" ')
print('To add to-do: python todo.py add_todo "TASK" "PROJECT ID" ')
print('To show all to-dos: python todo.py show_all_todo "COMPLETE/ INCOMPLETE" "COLUMN TO BE SORTED" "ASC/ DESC"')
print('To show all users: python todo.py show_all_users')
print('To show all projects: python todo.py show_all_projects')
print('To show completed to-dos: python todo.py show_complete')
print('To show tasks in a project: python todo.py show_tasks_by_project "PROJECT ID"')
print('To show tasks assigned to specific user: python todo.py show_tasks_by_user "USER ID" "USER NAME"')
print('To show projects with tasks assigned to specific user: python todo.py staff')
print('To show users having no assignment: python todo.py who_to_fire')
print('######################################################')
print()

sql = """
    CREATE TABLE IF NOT EXISTS todos(
        id INTEGER PRIMARY KEY,
        todo_text TEXT NOT NULL,
        due_date TEXT NOT NULL,
        status TEXT DEFAULT 'Incomplete',
        user_id INTEGER,
        project_id INTEGER
    )
"""
cur.execute(sql)

sql = """
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY,
        user_name TEXT NOT NULL,
        user_email TEXT NOT NULL
    )
"""
cur.execute(sql)

sql = """
    CREATE TABLE IF NOT EXISTS projects(
        project_id INTEGER PRIMARY KEY,
        project_name TEXT NOT NULL,
        description TEXT NOT NULL,
        user_id INTEGER
    )
"""
cur.execute(sql)


def set_due_date():
    tday = datetime.date.today()
    wish_due_day = int(
        input("This task is due in how many days from now? "))
    tdelta = datetime.timedelta(days=wish_due_day)
    due_day = tday + tdelta
    return due_day


def add_todo(todo_text, project_id=None, user_id=None):
    due_date = set_due_date()
    sql = """
        INSERT INTO todos (todo_text, project_id, user_id, due_date)
        VALUES (?, ?, ?, ?)
    """
    print("You've just assigned user ID " + str(user_id) + " a task: " +
          todo_text + " which will be due in " + str(due_date))
    print()

    cur.execute(sql, (todo_text, project_id, user_id, due_date,))
    conn.commit()


def add_user(user_name, user_email):
    sql = """
        INSERT INTO users (user_name, user_email)
        VALUES (?, ?)
    """
    print("You've created user: " + user_name)
    print()

    cur.execute(sql, (user_name, user_email,))
    conn.commit()


def add_project(project_name, description, user_id=None):
    sql = """
        INSERT INTO projects (project_name, description, user_id)
        VALUES (?, ?, ?)
    """
    print("You've created a project: " + project_name +
          " and assigned it to user ID " + str(user_id))
    print()

    cur.execute(sql, (project_name, description, user_id))
    conn.commit()


def mark_complete(id=0, todo_text="0"):
    sql = """
        UPDATE todos
        SET status = "Complete"
        WHERE id = ?
        OR todo_text = ?
    """
    cur.execute(sql, (id, todo_text,))
    conn.commit()


def show_all_todo(value=None, col="due_date", order="ASC"):
    if value == None:
        sql = """
            SELECT * FROM todos
            ORDER BY {} {} 
        """.format(col, order)
        cur.execute(sql)
        conn.commit()
        results = cur.fetchall()
        for row in results:
            print(row)
            print()

    else:
        sql = """
            SELECT * FROM todos
            WHERE {} LIKE "%{}%"
            ORDER BY {} {} 
        """.format(col, value, col, order)
        cur.execute(sql)
        conn.commit()
        results = cur.fetchall()
        for row in results:
            print(row)
        print()


def show_all_project():
    sql = """
            SELECT * FROM projects
        """
    cur.execute(sql)
    conn.commit()
    results = cur.fetchall()
    for row in results:
        print(row)
    print()


def show_all_users():
    sql = """
            SELECT * FROM users
        """
    cur.execute(sql)
    conn.commit()
    results = cur.fetchall()
    for row in results:
        print(row)
    print()


def show_complete():
    sql = """
        SELECT * FROM todos
        WHERE status = "Complete"
    """
    cur.execute(sql)
    conn.commit()
    results = cur.fetchall()
    for row in results:
        print(row)
    print()


def show_tasks_by_project(project_id):
    sql = """
        SELECT todos.todo_text, todos.due_date, todos.status, projects.project_name
        FROM todos
        INNER JOIN projects
        ON todos.project_id = projects.project_id
        WHERE projects.project_id = ?
    """
    cur.execute(sql, (project_id,))
    conn.commit()
    results = cur.fetchall()
    for row in results:
        print(row)
    print()


def show_tasks_by_user(user_id=None, user_name=None):
    sql = """
        SELECT todos.todo_text, todos.due_date, todos.status, users.user_name
        FROM todos
        INNER JOIN users
        ON todos.user_id = users.user_id
        WHERE users.user_id = ?
        OR users.user_name = ?
    """
    cur.execute(sql, (user_id, user_name,))
    conn.commit()
    results = cur.fetchall()
    for row in results:
        print(row)
    print()


def show_projects_by_user(user_id):
    sql = """
        SELECT * FROM projects
        INNER JOIN users
        ON projects.user_id = users.user_id
        WHERE projects.user_id = ?
    """
    cur.execute(sql, (user_id,))
    conn.commit()
    results = cur.fetchall()
    for row in results:
        print(row)
    print()


def staff():
    sql = """
        SELECT projects.project_name, users.user_name, todos.todo_text, todos.due_date, todos.status
        FROM projects
        INNER JOIN todos
        ON todos.project_id = projects.project_id
        INNER JOIN users
        ON todos.user_id = users.user_id
    """
    cur.execute(sql)
    conn.commit()
    results = cur.fetchall()
    for row in results:
        print(row)
    print()


def who_to_fire():
    sql = """
        SELECT DISTINCT users.user_name
        FROM users
        LEFT JOIN todos
        ON todos.user_id = users.user_id
        WHERE todos.user_id IS NULL
    """
    cur.execute(sql)
    conn.commit()
    results = cur.fetchall()
    for row in results:
        print(row)
    print()


if __name__ == '__main__':
    fire.Fire({
        "add_todo": add_todo,
        "show_all_todo": show_all_todo,
        "mark_complete": mark_complete,
        "show_complete": show_complete,
        "show_tasks_by_project": show_tasks_by_project,
        "add_user": add_user,
        "add_project": add_project,
        "show_all_projects": show_all_project,
        "show_all_users": show_all_users,
        "show_tasks_by_user": show_tasks_by_user,
        "show_projects_by_user": show_projects_by_user,
        "staff": staff,
        "who_to_fire": who_to_fire
    })

conn.close()
