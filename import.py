import csv
import os
import sqlite3

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        con = sqlite3.connect(db_file, check_same_thread=False)
        return con
    except sqlite3.Error as e:
        print(e)

    return None

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except sqlite3.Error as e:
        print(e)


def main():
    f=open("books.csv")
    conn = create_connection("books1.db")
    sql_create_books_table = """ CREATE TABLE books (
                                            isbn text,
                                            title text,
                                            author text,
                                            year text
                                        ); """

    sql_create_users_table = """ CREATE TABLE users (
                                                id integer primary key,
                                                username text not null,
                                                password text
                                            ); """
    create_table(conn, sql_create_users_table)
    create_table(conn, sql_create_books_table)
    reader = csv.reader(f)
    i = 0
    for isbn, title, author, year in reader:
        i = i + 1
        if i == 1:
            continue
        sql = ''' INSERT INTO books
                      VALUES(?, ?, ?, ?) '''
        cur = conn.cursor()
        cur.execute(sql, (str(isbn), str(title), str(author), str(year)))

    cur = conn.cursor()
    cur.execute("SELECT * FROM books")

    rows = cur.fetchall()
    print(rows[1])
    print(len(rows))
    conn.commit()
    conn.close()




if __name__=="__main__":
    main()

#def main():
#   f = open("flights.csv")
#   reader = csv.reader(f)
#   for origin, destination, duration in reader:
#        db.execute("INSERT INTO flights (origin, destination, duration) VALUES (:origin, :destination, :duration)",
#                    {"origin": origin, "destination": destination, "duration": duration})
#        print(f"Added flight from {origin} to {destination} lasting {duration} minutes.")
#    db.commit()