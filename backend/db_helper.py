import mysql.connector
from contextlib import  contextmanager
from logging_setup import logger_setup

logger = logger_setup('db_helper')

@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password ="password",
        database= "expense_manager"
    )
    if connection.is_connected():
        print("Connection is Successful")
    else:
        print("Failed")
    cursor = connection.cursor(dictionary=True)
    yield cursor

    if commit:
        connection.commit()
    cursor.close()
    connection.close()

def fetch_expense_for_date(expense_date):
    logger.info(f"fetch_expense_for_date called with: {expense_date}")
    with get_db_cursor(commit=False) as cursor:
        cursor.execute("Select * from expenses where expense_date = %s", (expense_date,))
        return cursor.fetchall()

def delete_expense_for_date(expense_date):
    logger.info(f"delete_expense_for_date called with: {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("Delete from expenses where expense_date = %s", (expense_date,))

def insert_expenses(expense_date, amount, category, notes):
    logger.info(f"insert_expenses called with: {expense_date, amount, category, notes}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s,%s,%s,%s)",
                       (expense_date,amount, category, notes))

def fetch_expense_summary(sdate,edate):
    logger.info(f"fetch_expense_summary called with start date: {sdate} and end Date: {edate}")
    with get_db_cursor(commit=False) as cursor:
        cursor.execute("select category,sum(amount) as total from expenses where expense_date between %s and %s group by category",
                       (sdate,edate,))
        data = cursor.fetchall()
        return data

def fetch_expense_summary_by_month():
    logger.info(f"fetch_expense_summary_by_month called")
    with get_db_cursor(commit=False) as cursor:
        cursor.execute("select date_format(expense_date, '%b %Y') AS expense_month,sum(amount) as total from expenses group by expense_month order by expense_month")
        data = cursor.fetchall()
        return data

def get_max_expense_date():
    logger.info(f"get_max_expense_date called")
    with get_db_cursor(commit=False) as cursor:
        cursor.execute("SELECT MAX(expense_date) as last_expense_date from expenses")
        data = cursor.fetchall()
        return data


if __name__ == "__main__":
    expenses= get_max_expense_date()
    print(expenses[0]['last_expense_date'])



