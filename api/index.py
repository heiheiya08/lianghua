
from fastapi import FastAPI
import pandas as pd
import akshare as ak

app = FastAPI()

@app.get("/backtest")
def backtest(code: str = "sh600519"):
    df = ak.stock_zh_a_hist(symbol=code, period="daily", adjust="qfq")

    df = df[["日期", "开盘", "收盘"]]
    df.columns = ["date", "open", "close"]

    start = float(df["close"].iloc[0])
    end = float(df["close"].iloc[-1])

    return {
        "code": code,
        "start": start,
        "end": end,
        "return_pct": float((end - start) / start * 100)
    }
