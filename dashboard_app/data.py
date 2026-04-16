from pathlib import Path

import pandas as pd


def load_marketing_data(project_root: Path) -> pd.DataFrame:
    csv_path = project_root / "Marketing.csv"
    df = pd.read_csv(csv_path)
    df["c_date"] = pd.to_datetime(df["c_date"])
    return df


def compute_kpis(df: pd.DataFrame) -> dict:
    total_impressions = int(df["impressions"].sum())
    total_clicks = int(df["clicks"].sum())
    total_leads = int(df["leads"].sum())
    total_revenue = float(df["revenue"].sum())
    total_spent = float(df["mark_spent"].sum())
    total_orders = int(df["orders"].sum())

    roas = total_revenue / total_spent if total_spent > 0 else 0.0
    ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0.0
    conversion_rate = (total_orders / total_clicks * 100) if total_clicks > 0 else 0.0

    return {
        "total_impressions": total_impressions,
        "total_clicks": total_clicks,
        "total_leads": total_leads,
        "total_revenue": total_revenue,
        "total_spent": total_spent,
        "total_orders": total_orders,
        "roas": roas,
        "ctr": ctr,
        "conversion_rate": conversion_rate,
    }
