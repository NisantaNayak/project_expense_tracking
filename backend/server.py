from datetime import date
from typing import List
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
import db_helper


class Expense(BaseModel):
    amount: float
    category: str
    notes: str
class DateRange(BaseModel):
    start_date: date
    end_date: date

app=FastAPI()


@app.get("/expenses/{expense_date}",response_model=List[Expense])
def get_expense(expense_date:date):
    expenses = db_helper.fetch_expense_for_date(expense_date)
    if expenses is None:
        raise HTTPException(status_code=500, detail ="Failed to retrieve expense summary from database")
    return expenses


@app.post("/expenses/{expense_date}")
def add_or_update_expenses(expense_date: date, expenses: List[Expense]):
    print(f"Received date: {expense_date}, expenses: {expenses}")
    db_helper.delete_expense_for_date(expense_date)
    for expense in expenses:
        db_helper.insert_expenses(expense_date, expense.amount, expense.category, expense.notes)
    return {"message": "Expenses received successfully"}

@app.post("/analytics/")
def get_analytics(date_range:DateRange):
    data= db_helper.fetch_expense_summary(date_range.start_date,date_range.end_date)
    if data is None:
        raise HTTPException(status_code=500, detail ="Failed to retrieve expense summary from database")
    #return data
    total=0
    for row in data:
        total = total+row['total']
    breakdown= {}
    for row in data:
        percentage = (row['total']/total)*100 if total!= 0 else 0
        breakdown[row['category']]= {
            "total" : row['total'],
            "percentage": percentage
        }
    return breakdown

@app.get("/analytics_by_month/")
def get_analytics_by_month():
    data = db_helper.fetch_expense_summary_by_month()
    if data is None:
        raise HTTPException(status_code=500, detail ="Failed to retrieve expense summary from database")
    total=0
    for row in data:
        total = total+row['total']
    breakdown= {}
    for row in data:
        breakdown[row['expense_month']]= {
            "total" : row['total']
        }
    return breakdown

@app.get("/expense/date")
def get_max_expense_date():
    data = db_helper.get_max_expense_date()
    if data is None:
        raise HTTPException(status_code=500, detail ="Failed to retrieve expense summary from database")
    return data
