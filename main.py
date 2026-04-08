from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import mysql.connector

app = FastAPI()

# ─────────────────────────────────────────
#  ตั้งค่าการเชื่อมต่อ MariaDB
#  แก้ user และ password ให้ตรงกับเครื่องของคุณ
# ─────────────────────────────────────────
DB_CONFIG = {
    "host":     "localhost",
    "port":     3306,
    "user":     "root",               # แก้ตามจริง
    "password": "",      # แก้ตามจริง
    "database": "sales_management_system",
}

class SaleCreate(BaseModel):
    employee_id: int
    amount: float

def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)

def execute_query(query, params=None):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params or ())
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def execute_write(query, params=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params or ())
    conn.commit()
    cursor.close()
    conn.close()

# ─────────────────────────────────────────
#  Endpoints
# ─────────────────────────────────────────
@app.get("/employees")
def get_employees():
    return execute_query(
        "SELECT employee_id, name FROM employees ORDER BY name"
    )

@app.get("/sales/summary")
def get_sales_summary():
    query = """
    SELECT
        e.employee_id,
        e.name,
        e.position,
        SUM(s.amount)                             AS total_sales,
        (SUM(s.amount) * e.commission_rate / 100) AS commission
    FROM employees e
    JOIN sales s ON e.employee_id = s.employee_id
    GROUP BY e.employee_id, e.name, e.position, e.commission_rate
    ORDER BY total_sales DESC
    """
    return execute_query(query)

@app.get("/sales/daily")
def get_daily_sales():
    """ยอดขายรายวัน 30 วันล่าสุด"""
    query = """
    SELECT
        sale_date       AS date,
        SUM(amount)     AS total
    FROM sales
    WHERE sale_date >= CURDATE() - INTERVAL 29 DAY
    GROUP BY sale_date
    ORDER BY sale_date ASC
    """
    return execute_query(query)

@app.get("/sales/monthly")
def get_monthly_sales():
    """ยอดขายรายเดือน 12 เดือนล่าสุด"""
    query = """
    SELECT
        DATE_FORMAT(sale_date, '%Y-%m')  AS month,
        SUM(amount)                      AS total
    FROM sales
    WHERE sale_date >= CURDATE() - INTERVAL 365 DAY
    GROUP BY DATE_FORMAT(sale_date, '%Y-%m')
    ORDER BY month ASC
    """
    return execute_query(query)

@app.get("/sales/yearly")
def get_yearly_sales():
    """ยอดขายรายปี ทุกปี"""
    query = """
    SELECT
        YEAR(sale_date)  AS year,
        SUM(amount)      AS total
    FROM sales
    GROUP BY YEAR(sale_date)
    ORDER BY year ASC
    """
    return execute_query(query)

@app.post("/sales")
def create_sale(sale: SaleCreate):
    try:
        execute_write(
            "INSERT INTO sales (employee_id, amount, sale_date) VALUES (%s, %s, CURDATE())",
            (sale.employee_id, sale.amount),
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": "Success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)