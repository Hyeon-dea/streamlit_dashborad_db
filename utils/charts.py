import plotly.express as px

def sales_by_category_chart(df):
    temp = df.copy()
    temp["amount"] = temp["quantity"] * temp["price"]
    grouped = temp.groupby("category", as_index=False)["amount"].sum()

    fig = px.bar(
        grouped,
        x="category",
        y="amount",
        title="카테고리별 총매출"
    )
    return fig

def sales_by_region_chart(df):
    temp = df.copy()
    temp["amount"] = temp["quantity"] * temp["price"]
    grouped = temp.groupby("region", as_index=False)["amount"].sum()

    fig = px.pie(
        grouped,
        names="region",
        values="amount",
        title="지역별 매출 비중"
    )
    return fig

def sales_trend_chart(df):
    temp = df.copy()
    temp["amount"] = temp["quantity"] * temp["price"]
    grouped = temp.groupby("order_date", as_index=False)["amount"].sum()

    fig = px.line(
        grouped,
        x="order_date",
        y="amount",
        title="일자별 매출 추이"
    )
    return fig