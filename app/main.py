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

@app.get("/defects")
def filter_defects(
    product_id: Optional[str] = Query(None),
    severity: Optional[str] = Query(None),
    from_date: Optional[date] = Query(None),
    to_date: Optional[date] = Query(None),
):
    df = load_defect_data()

    if product_id:
        df = df[df["product_id"] == product_id]
    if severity:
        df = df[df["severity"] == severity]
    if from_date:
        from_dt = pd.to_datetime(from_date)
        df = df[df["defect_date"] >= from_dt]
    if to_date:
        to_dt = pd.to_datetime(to_date)
        df = df[df["defect_date"] <= to_dt]

    return df.to_dict(orient="records")

@app.get("/summary")
def get_summary(
    products: Optional[list[str]] = Query(default=None),
    defect_types: Optional[list[str]] = Query(default=None),
    locations: Optional[list[str]] = Query(default=None),
    from_date: Optional[str] = Query(default=None),
    to_date: Optional[str] = Query(default=None),
):
    df = data.copy()

    # 🧮 Apply filters
    if products:
        df = df[df["product_id"].isin(products)]
    if defect_types:
        df = df[df["defect_type"].isin(defect_types)]
    if locations:
        df = df[df["defect_location"].isin(locations)]
    if from_date:
        df = df[df["defect_date"] >= pd.to_datetime(from_date)]
    if to_date:
        df = df[df["defect_date"] <= pd.to_datetime(to_date)]

    result = []

    for pid, group in df.groupby("product_id"):
        total_defects = len(group)
        total_repair_cost = group["repair_cost"].sum()

        severity_counts = group["severity"].value_counts().to_dict()
        average_costs = group.groupby("severity")["repair_cost"].mean().round(2).to_dict()

        result.append({
            "product_id": pid,
            "total_defects": total_defects,
            "total_repair_cost": round(total_repair_cost, 2),
            "severity_counts": severity_counts,
            "average_costs": average_costs
        })

    return result