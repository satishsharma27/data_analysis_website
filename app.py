import dash
from dash import dcc, html, callback, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import os
from flask import Flask, render_template

# ═════════════════════════════════════════════════════════════════════════════
# FLASK APP SETUP
# ═════════════════════════════════════════════════════════════════════════════
server = Flask(__name__)
server.config['PROPAGATE_EXCEPTIONS'] = True

@server.route("/")
def home():
    return render_template("index.html")

@server.route("/data-analysis")
def data_analysis():
    return render_template("data-analysis.html")

# ═════════════════════════════════════════════════════════════════════════════
# DASHBOARD DATA & SETUP
# ═════════════════════════════════════════════════════════════════════════════

csv_path = os.path.join(os.path.dirname(__file__), "Marketing.csv")
df = pd.read_csv(csv_path)
df['c_date'] = pd.to_datetime(df['c_date'])

# Color scheme
FONT   = "Arial, Helvetica Neue, sans-serif"
BORDER = "#E8E6E0"
TEXT   = "#2C2C2A"
MUTED  = "#888780"
BLUE   = "#378ADD"
TEAL   = "#1D9E75"
CARD   = "#FFFFFF"
AMBER  = "#BA7517"
PINK   = "#D4537E"
PURPLE = "#7F77DD"
GREEN  = "#3B6D11"

# Color mapping for categories
CATEGORY_COLORS = {
    "social": "#378ADD",
    "search": "#1D9E75",
    "influencer": "#BA7517",
    "media": "#D4537E"
}

# ── Aggregated Data ───────────────────────────────────────────────────────────
total_impressions = df['impressions'].sum()
total_clicks = df['clicks'].sum()
total_leads = df['leads'].sum()
total_revenue = df['revenue'].sum()
total_spent = df['mark_spent'].sum()
total_orders = df['orders'].sum()
roas = total_revenue / total_spent if total_spent > 0 else 0
ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
conversion_rate = (total_orders / total_clicks * 100) if total_clicks > 0 else 0

# ── Chart Functions ──────────────────────────────────────────────────────────
def trend_chart(category_filter=None):
    """Revenue trend over time by category"""
    filtered_df = df
    if category_filter and category_filter != "All":
        filtered_df = df[df['category'] == category_filter]
    
    daily_revenue = filtered_df.groupby('c_date').agg({
        'revenue': 'sum',
        'clicks': 'sum',
        'orders': 'sum'
    }).reset_index()
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily_revenue['c_date'], y=daily_revenue['revenue'],
        name="Revenue",
        mode="lines+markers",
        line=dict(color=BLUE, width=2.5),
        marker=dict(size=4),
        fill="tozeroy", fillcolor="rgba(55,138,221,0.1)",
        hovertemplate="<b>%{x|%b %d}</b><br>Revenue: $%{y:,.0f}<extra></extra>",
    ))
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
        font=dict(family=FONT, color=TEXT, size=11),
        xaxis=dict(showgrid=False, tickfont=dict(size=10), color=MUTED,
                   zeroline=False, showline=False),
        yaxis=dict(showgrid=True, gridcolor=BORDER, gridwidth=0.5,
                   tickfont=dict(size=10), color=TEXT, zeroline=False,
                   showline=False, tickformat="$,.0f"),
        hovermode="x unified",
        height=240,
    )
    return fig


def category_donut():
    """Traffic by category"""
    category_data = df.groupby('category').agg({
        'clicks': 'sum'
    }).reset_index()
    
    fig = go.Figure(go.Pie(
        labels=category_data['category'].str.capitalize(),
        values=category_data['clicks'],
        hole=0.62,
        marker=dict(
            colors=[CATEGORY_COLORS.get(cat, PURPLE) for cat in category_data['category']],
            line=dict(color=CARD, width=2)
        ),
        textinfo="none",
        hovertemplate="<b>%{label}</b><br>Clicks: %{value:,.0f}<extra></extra>",
        direction="clockwise", sort=False,
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=120, t=10, b=10),
        font=dict(family=FONT, color=TEXT, size=11),
        legend=dict(orientation="v", yanchor="middle", y=0.5,
                    xanchor="left", x=0.78, font=dict(size=10),
                    bgcolor="rgba(0,0,0,0)", itemsizing="constant"),
        showlegend=True,
        height=240,
        annotations=[dict(
            text="Clicks by<br>Category", x=0.38, y=0.5,
            font=dict(size=11, color=MUTED, family=FONT),
            showarrow=False, xanchor="center",
        )],
    )
    return fig


def campaign_performance():
    """Top campaigns by revenue"""
    campaign_data = df.groupby('campaign_name').agg({
        'revenue': 'sum',
        'mark_spent': 'sum',
        'orders': 'sum'
    }).reset_index()
    campaign_data['roas'] = campaign_data['revenue'] / campaign_data['mark_spent']
    campaign_data = campaign_data.nlargest(8, 'revenue')
    
    fig = go.Figure(go.Bar(
        y=campaign_data['campaign_name'],
        x=campaign_data['revenue'],
        orientation="h",
        marker=dict(color=TEAL, line=dict(width=0)),
        text=[f"${v:,.0f}" for v in campaign_data['revenue']],
        textposition="outside",
        textfont=dict(size=10, color=TEXT),
        hovertemplate="<b>%{y}</b><br>Revenue: $%{x:,.0f}<extra></extra>",
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=120, r=40, t=10, b=10),
        font=dict(family=FONT, color=TEXT, size=10),
        xaxis=dict(showgrid=True, gridcolor=BORDER, gridwidth=0.5,
                   tickfont=dict(size=9), color=MUTED, zeroline=False,
                   showline=False, tickformat="$,.0f"),
        yaxis=dict(showgrid=False, tickfont=dict(size=10), color=TEXT,
                   zeroline=False, showline=False),
        bargap=0.4,
        height=240,
    )
    return fig


def category_comparison():
    """Category performance metrics"""
    category_metrics = df.groupby('category').agg({
        'impressions': 'sum',
        'clicks': 'sum',
        'orders': 'sum',
        'revenue': 'sum',
        'mark_spent': 'sum'
    }).reset_index()
    category_metrics['roas'] = category_metrics['revenue'] / category_metrics['mark_spent']
    
    fig = go.Figure(data=[
        go.Bar(name='Revenue', x=category_metrics['category'].str.capitalize(),
               y=category_metrics['revenue'], marker_color=BLUE, yaxis="y"),
        go.Bar(name='Orders', x=category_metrics['category'].str.capitalize(),
               y=category_metrics['orders'], marker_color=TEAL, yaxis="y2"),
    ])
    
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=50, t=10, b=10),
        font=dict(family=FONT, color=TEXT, size=11),
        xaxis=dict(showgrid=False, tickfont=dict(size=10), color=MUTED,
                   zeroline=False, showline=False),
        yaxis=dict(showgrid=True, gridcolor=BORDER, gridwidth=0.5,
                   tickfont=dict(size=9), color=BLUE, zeroline=False,
                   showline=False, tickformat="$,.0f",
                   title=dict(text="Revenue", font=dict(color=BLUE, size=10))),
        yaxis2=dict(showgrid=False, tickfont=dict(size=9), color=TEAL,
                    zeroline=False, showline=False, overlaying="y",
                    side="right", tickformat=".0f",
                    title=dict(text="Orders", font=dict(color=TEAL, size=10))),
        barmode="group",
        height=240,
        hovermode="x unified",
    )
    return fig


# ── Component helpers ─────────────────────────────────────────────────────────
def kpi_card(label, value, delta, up=True):
    arrow = "▲" if up else "▼"
    return html.Div([
        html.P(label,               className="kpi-label"),
        html.P(value,               className="kpi-value"),
        html.P(f"{arrow} {delta}",  className=f"kpi-delta {'up' if up else 'down'}"),
    ], className="kpi-card")


def format_currency(value):
    """Format number as currency"""
    return f"${value:,.0f}"


def format_number(value):
    """Format large number with K/M suffix"""
    if value >= 1_000_000:
        return f"{value/1_000_000:.1f}M"
    elif value >= 1_000:
        return f"{value/1_000:.1f}K"
    return f"{value:.0f}"


# ═════════════════════════════════════════════════════════════════════════════
# DASH APP SETUP - INTEGRATED WITH FLASK
# ═════════════════════════════════════════════════════════════════════════════

app = dash.Dash(__name__, server=server, url_base_pathname="/dashboard/", 
                title="Marketing Dashboard", suppress_callback_exceptions=True)

app.layout = html.Div([
    # Header
    html.Div([
        html.Div([
            html.H1("Marketing Dashboard"),
            html.P(f"Feb 2021 - {df['c_date'].max().strftime('%b %Y')}", className="subtitle"),
        ]),
        html.Div("● Active", className="live-badge"),
    ], className="header"),

    html.Hr(className="divider"),

    # Filter Section
    html.Div([
        html.P("Filters", className="section-label"),
        html.Div([
            html.Div([
                html.Label("Category:", style={"fontWeight": "600", "fontSize": "12px"}),
                dcc.Dropdown(
                    id="category-filter",
                    options=[{"label": "All Categories", "value": "All"}] + 
                            [{"label": cat.capitalize(), "value": cat} for cat in df['category'].unique()],
                    value="All",
                    style={"width": "100%"}
                ),
            ], style={"marginRight": "15px", "flex": "1", "minWidth": "150px"}),
        ], style={"display": "flex", "gap": "10px", "marginBottom": "15px"}),
    ]),

    # KPIs
    html.P("Key Metrics", className="section-label"),
    html.Div([
        kpi_card("Total Impressions", format_number(total_impressions), f"{ctr:.1f}% CTR", True),
        kpi_card("Total Clicks", format_number(total_clicks), f"{conversion_rate:.1f}% Conv Rate", True),
        kpi_card("Total Revenue", format_currency(total_revenue), f"{roas:.2f}x ROAS", True),
        kpi_card("Marketing Spend", format_currency(total_spent), f"{(total_spent/total_revenue*100):.1f}% ACOS", False),
    ], className="kpi-row"),

    # Charts row
    html.P("Performance Overview", className="section-label"),
    html.Div([
        html.Div([
            html.P("Revenue Trend", className="card-title"),
            dcc.Graph(id="trend-chart", config={"displayModeBar": False},
                      style={"height": "240px"}),
        ], className="card card-trend"),
        html.Div([
            html.P("Clicks by Category", className="card-title"),
            dcc.Graph(figure=category_donut(), config={"displayModeBar": False},
                      style={"height": "240px"}),
        ], className="card card-donut"),
    ], className="charts-row"),

    # Bottom row
    html.P("Campaign Analysis", className="section-label"),
    html.Div([
        html.Div([
            html.P("Top Campaigns by Revenue", className="card-title"),
            dcc.Graph(figure=campaign_performance(), config={"displayModeBar": False},
                      style={"height": "240px"}),
        ], className="card card-campaign"),
        html.Div([
            html.P("Category Comparison", className="card-title"),
            dcc.Graph(figure=category_comparison(), config={"displayModeBar": False},
                      style={"height": "240px"}),
        ], className="card card-channel"),
    ], className="bottom-row"),

    # Footer
    html.Hr(className="divider", style={"marginTop": "20px"}),
    html.P(
        f"Marketing Dashboard  ·  Data Period: Feb 2021 - {df['c_date'].max().strftime('%b %Y')}  ·  Total Records: {len(df)}",
        className="footer",
    ),

], className="dashboard")

# ── Add dashboard styles ──────────────────────────────────────────────────────
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        <link rel="stylesheet" href="/static/dashboard-style.css">
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# ── Callbacks ─────────────────────────────────────────────────────────────────
@app.callback(
    Output("trend-chart", "figure"),
    Input("category-filter", "value")
)
def update_trend_chart(selected_category):
    return trend_chart(selected_category)


# ═════════════════════════════════════════════════════════════════════════════
# PRODUCTION SETUP
# ═════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Production: disable debug mode
    server.run(debug=False, port=5001, host="0.0.0.0")