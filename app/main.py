from fastapi import FastAPI, Query
from app.data_loader import load_defect_data
from typing import Optional
from datetime import date
import pandas as pd

app = FastAPI()
data = load_defect_data()

@app.get("/products")
def get_products():
    return {"products": data['product_id'].unique().tolist()}

@app.get("/defects", tags=["Defects"], summary="Filter defects")
def filter_defects(
    product_id: Optional[str] = Query(None, description="Filter by product ID"),
    severity: Optional[str] = Query(None, description="Filter by severity"),
    start_date: Optional[date] = Query(None, description="Start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="End date (YYYY-MM-DD)")
):
    df = load_defect_data()

    if product_id:
        df = df[df["product_id"] == product_id]
    if severity:
        df = df[df["severity"] == severity]
    if start_date:
        df = df[df["defect_date"] >= start_date]
    if end_date:
        df = df[df["defect_date"] <= end_date]

    return df.to_dict(orient="records")

@app.get("/summary")
def get_summary(
    products: list[str] | None = Query(None),
    from_date: str | None = None,
    to_date: str | None = None
):
    df = data.copy()
    if products:
        df = df[df["product_id"].isin(products)]
    if from_date:
        df = df[df["defect_date"] >= pd.to_datetime(from_date)]
    if to_date:
        df = df[df["defect_date"] <= pd.to_datetime(to_date)]

    summary = df.groupby("product_id").agg(
        total_defects=("defect_id", "count"),
        total_repair_cost=("repair_cost", "sum"),
    )

    severity_counts = df.groupby(["product_id", "severity"]).size().unstack(fill_value=0)
    avg_cost_severity = df.groupby(["product_id", "severity"])["repair_cost"].mean().unstack(fill_value=0)

    result = summary.join(severity_counts, rsuffix="_count").join(avg_cost_severity, rsuffix="_avg_cost")
    return result.reset_index().to_dict(orient="records")
