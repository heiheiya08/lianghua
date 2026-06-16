
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import akshare as ak

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def home():
    return """<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>量化系统</title>
<script src="https://cdn.jsdelivr.net/npm/echarts/dist/echarts.min.js"></script>
</head>

<body style="font-family:Arial;padding:20px;">
<h2>📊 量化回测系统</h2>

<input id="code" placeholder="sh600519"/>
<button onclick="run()">回测</button>

<h3 id="result"></h3>
<div id="chart" style="width:100%;height:500px;"></div>

<script>
async function run(){
    const code=document.getElementById('code').value;

    const res=await fetch('/backtest?code='+code);
    const data=await res.json();

    document.getElementById('result').innerText =
    '收益率: ' + data.return_pct.toFixed(2) + '%';

    const chart = echarts.init(document.getElementById('chart'));
    chart.setOption({
        xAxis:{type:'category',data:['start','end']},
        yAxis:{type:'value'},
        series:[{type:'line',data:[data.start,data.end]}]
    });
}
</script>

</body>
</html>"""

@app.get("/backtest")
def backtest(code: str = "sh600519"):
    df = ak.stock_zh_a_hist(symbol=code, period="daily", adjust="qfq")

    start = float(df["收盘"].iloc[0])
    end = float(df["收盘"].iloc[-1])

    return {
        "code": code,
        "start": start,
        "end": end,
        "return_pct": float((end-start)/start*100)
    }
