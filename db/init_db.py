import pandas as pd
from sqlalchemy import text
from db.connection import get_engine

def create_table_customer():
    engine = get_engine()

    create_sql = """
    CREATE TABLE IF NOT EXISTS customers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        region VARCHAR(50) NOT NULL,
        age INT NOT NULL,
        join_date DATE NOT NULL,
        sales DECIMAL(12,2) NOT NULL
    )
    """

    with engine.begin() as conn:
        conn.execute(text(create_sql))


def seed_customer_data():
    engine = get_engine()

    check_sql = "SELECT COUNT(*) AS cnt FROM customers"
    with engine.begin() as conn:
        cnt = conn.execute(text(check_sql)).scalar()

        if cnt == 0:
            sample = pd.DataFrame([
                ["김민수", "서울", 29, "2024-01-15", 120000],
                ["이서연", "부산", 34, "2024-02-10", 250000],
                ["박지훈", "대구", 41, "2024-03-05", 180000],
                ["최유리", "서울", 26, "2024-03-12", 95000],
                ["정하늘", "인천", 38, "2024-04-01", 310000],
                ["한지민", "부산", 31, "2024-04-18", 210000],
                ["오세훈", "광주", 45, "2024-05-07", 415000],
                ["서은우", "대전", 28, "2024-05-12", 87000],
                ["윤도현", "서울", 36, "2024-06-03", 275000],
                ["강수진", "인천", 33, "2024-06-22", 143000],
            ], columns=["name", "region", "age", "join_date", "sales"])

            sample.to_sql("customers", con=engine, if_exists="append", index=False)