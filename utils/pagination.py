import math
import pandas as pd

def paginate_df(df: pd.DataFrame, page_number: int, page_size: int):
    total_rows = len(df)
    total_pages = max(1, math.ceil(total_rows / page_size))

    if page_number < 1:
        page_number = 1
    if page_number > total_pages:
        page_number = total_pages

    start_idx = (page_number - 1) * page_size
    end_idx = start_idx + page_size

    page_df = df.iloc[start_idx:end_idx].copy()
    return page_df, total_pages