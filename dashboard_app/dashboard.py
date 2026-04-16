from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go

from .data import compute_kpis
from .utils import (
    BLUE,
    BORDER,
    CARD,
    CATEGORY_COLORS,
    FONT,
    MUTED,
    PINK,
    TEAL,
    TEXT,
    format_currency,
    format_number,
)


def trend_chart(df, category_filter="All"):
    filtered_df = df if category_filter == "All" else df[df["category"] == category_filter]
    daily_revenue = filtered_df.groupby("c_date").agg({
        "revenue": "sum",
        "clicks": "sum",
        "orders": "sum",
    }).reset_index()

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=daily_revenue["c_date"],
        y=daily_revenue["revenue"],
        name="Revenue",
        mode="lines+markers",
        line=dict(color=BLUE, width=2.5),
        marker=dict(size=4),
        fill="tozeroy",
        fillcolor="rgba(55,138,221,0.1)",
        hovertemplate="<b>%{x|%b %d}</b><br>Revenue: $%{y:,.0f}<extra></extra>",
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=10, b=10),
        font=dict(family=FONT, color=TEXT, size=11),
        xaxis=dict(showgrid=False, tickfont=dict(size=10), color=MUTED, zeroline=False, showline=False),
        yaxis=dict(
            showgrid=True,
            gridcolor=BORDER,
            gridwidth=0.5,
            tickfont=dict(size=10),
            color=TEXT,
            zeroline=False,
            showline=False,
            tickformat="$,.0f",
        ),
        hovermode="x unified",
        height=240,
    )
    return fig


def category_donut(df):
    category_data = (
        df.groupby("category").agg({"clicks": "sum"}).reset_index()
    )

    fig = go.Figure(go.Pie(
        labels=category_data["category"].str.capitalize(),
        values=category_data["clicks"],
        hole=0.62,
        marker=dict(
            colors=[CATEGORY_COLORS.get(cat, PINK) for cat in category_data["category"]],
            line=dict(color=CARD, width=2),
        ),
        textinfo="none",
        hovertemplate="<b>%{label}</b><br>Clicks: %{value:,.0f}<extra></extra>",
        direction="clockwise",
        sort=False,
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=120, t=10, b=10),
        font=dict(family=FONT, color=TEXT, size=11),
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=0.78,
            font=dict(size=10),
            bgcolor="rgba(0,0,0,0)",
            itemsizing="constant",
        ),
        showlegend=True,
        height=240,
        annotations=[
            dict(
                text="Clicks by<br>Category",
                x=0.38,
                y=0.5,
                font=dict(size=11, color=MUTED, family=FONT),
                showarrow=False,
                xanchor="center",
            )
        ],
    )
    return fig


def campaign_performance(df):
    campaign_data = (
        df.groupby("campaign_name")
        .agg({"revenue": "sum", "mark_spent": "sum", "orders": "sum"})
        .reset_index()
    )
    campaign_data["roas"] = campaign_data["revenue"] / campaign_data["mark_spent"].replace(0, 1)
    campaign_data = campaign_data.nlargest(8, "revenue")

    fig = go.Figure(go.Bar(
        y=campaign_data["campaign_name"],
        x=campaign_data["revenue"],
        orientation="h",
        marker=dict(color=TEAL, line=dict(width=0)),
        text=[f"${v:,.0f}" for v in campaign_data["revenue"]],
        textposition="outside",
        textfont=dict(size=10, color=TEXT),
        hovertemplate="<b>%{y}</b><br>Revenue: $%{x:,.0f}<extra></extra>",
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=120, r=40, t=10, b=10),
        font=dict(family=FONT, color=TEXT, size=10),
        xaxis=dict(
            showgrid=True,
            gridcolor=BORDER,
            gridwidth=0.5,
            tickfont=dict(size=9),
            color=MUTED,
            zeroline=False,
            showline=False,
            tickformat="$,.0f",
        ),
        yaxis=dict(
            showgrid=False,
            tickfont=dict(size=10),
            color=TEXT,
            zeroline=False,
            showline=False,
        ),
        bargap=0.4,
        height=240,
    )
    return fig


def category_comparison(df):
    category_metrics = (
        df.groupby("category")
        .agg({
            "impressions": "sum",
            "clicks": "sum",
            "orders": "sum",
            "revenue": "sum",
            "mark_spent": "sum",
        })
        .reset_index()
    )
    category_metrics["roas"] = category_metrics["revenue"] / category_metrics["mark_spent"].replace(0, 1)

    fig = go.Figure(data=[
        go.Bar(
            name="Revenue",
            x=category_metrics["category"].str.capitalize(),
            y=category_metrics["revenue"],
            marker_color=BLUE,
            yaxis="y",
        ),
        go.Bar(
            name="Orders",
            x=category_metrics["category"].str.capitalize(),
            y=category_metrics["orders"],
            marker_color=TEAL,
            yaxis="y2",
        ),
    ])

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=50, t=10, b=10),
        font=dict(family=FONT, color=TEXT, size=11),
        xaxis=dict(showgrid=False, tickfont=dict(size=10), color=MUTED, zeroline=False, showline=False),
        yaxis=dict(
            showgrid=True,
            gridcolor=BORDER,
            gridwidth=0.5,
            tickfont=dict(size=9),
            color=BLUE,
            zeroline=False,
            showline=False,
            tickformat="$,.0f",
            title=dict(text="Revenue", font=dict(color=BLUE, size=10)),
        ),
        yaxis2=dict(
            showgrid=False,
            tickfont=dict(size=9),
            color=TEAL,
            zeroline=False,
            showline=False,
            overlaying="y",
            side="right",
            tickformat=".0f",
            title=dict(text="Orders", font=dict(color=TEAL, size=10)),
        ),
        barmode="group",
        height=240,
        hovermode="x unified",
    )
    return fig


def kpi_card(label: str, value: str, delta: str, up: bool = True):
    arrow = "▲" if up else "▼"
    return html.Div(
        [
            html.P(label, className="kpi-label"),
            html.P(value, className="kpi-value"),
            html.P(f"{arrow} {delta}", className=f"kpi-delta {'up' if up else 'down'}"),
        ],
        className="kpi-card",
    )


def init_dashboard(server, df):
    metrics = compute_kpis(df)
    category_options = [
        {"label": "All Categories", "value": "All"},
    ] + [
        {"label": cat.capitalize(), "value": cat}
        for cat in sorted(df["category"].unique())
    ]

    dashboard = Dash(
        __name__,
        server=server,
        url_base_pathname="/dashboard/",
        title="Marketing Dashboard",
        suppress_callback_exceptions=True,
    )

    dashboard.layout = html.Div(
        [
            html.Div(
                [
                    html.Div(
                        [
                            html.H1("Marketing Dashboard"),
                            html.P(
                                f"Feb 2021 - {df['c_date'].max().strftime('%b %Y')}",
                                className="subtitle",
                            ),
                        ]
                    ),
                    html.Div("● Active", className="live-badge"),
                ],
                className="header",
            ),
            html.Hr(className="divider"),
            html.Div(
                [
                    html.P("Filters", className="section-label"),
                    html.Div(
                        [
                            html.Div(
                                [
                                    html.Label("Category:", style={"fontWeight": "600", "fontSize": "12px"}),
                                    dcc.Dropdown(
                                        id="category-filter",
                                        options=category_options,
                                        value="All",
                                        style={"width": "100%"},
                                    ),
                                ],
                                style={"marginRight": "15px", "flex": "1", "minWidth": "150px"},
                            ),
                        ],
                        style={"display": "flex", "gap": "10px", "marginBottom": "15px"},
                    ),
                ]
            ),
            html.P("Key Metrics", className="section-label"),
            html.Div(
                [
                    kpi_card("Total Impressions", format_number(metrics["total_impressions"]), f"{metrics['ctr']:.1f}% CTR", True),
                    kpi_card("Total Clicks", format_number(metrics["total_clicks"]), f"{metrics['conversion_rate']:.1f}% Conv Rate", True),
                    kpi_card("Total Revenue", format_currency(metrics["total_revenue"]), f"{metrics['roas']:.2f}x ROAS", True),
                    kpi_card(
                        "Marketing Spend",
                        format_currency(metrics["total_spent"]),
                        f"{(metrics['total_spent'] / metrics['total_revenue'] * 100 if metrics['total_revenue'] else 0.0):.1f}% ACOS",
                        False,
                    ),
                ],
                className="kpi-row",
            ),
            html.P("Performance Overview", className="section-label"),
            html.Div(
                [
                    html.Div(
                        [
                            html.P("Revenue Trend", className="card-title"),
                            dcc.Graph(
                                id="trend-chart",
                                config={"displayModeBar": False},
                                style={"height": "240px"},
                            ),
                        ],
                        className="card card-trend",
                    ),
                    html.Div(
                        [
                            html.P("Clicks by Category", className="card-title"),
                            dcc.Graph(
                                figure=category_donut(df),
                                config={"displayModeBar": False},
                                style={"height": "240px"},
                            ),
                        ],
                        className="card card-donut",
                    ),
                ],
                className="charts-row",
            ),
            html.P("Campaign Analysis", className="section-label"),
            html.Div(
                [
                    html.Div(
                        [
                            html.P("Top Campaigns by Revenue", className="card-title"),
                            dcc.Graph(
                                figure=campaign_performance(df),
                                config={"displayModeBar": False},
                                style={"height": "240px"},
                            ),
                        ],
                        className="card card-campaign",
                    ),
                    html.Div(
                        [
                            html.P("Category Comparison", className="card-title"),
                            dcc.Graph(
                                figure=category_comparison(df),
                                config={"displayModeBar": False},
                                style={"height": "240px"},
                            ),
                        ],
                        className="card card-channel",
                    ),
                ],
                className="bottom-row",
            ),
            html.Hr(className="divider", style={"marginTop": "20px"}),
            html.P(
                f"Marketing Dashboard  ·  Data Period: Feb 2021 - {df['c_date'].max().strftime('%b %Y')}  ·  Total Records: {len(df)}",
                className="footer",
            ),
        ],
        className="dashboard",
    )

    dashboard.index_string = '''
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

    @dashboard.callback(
        Output("trend-chart", "figure"),
        Input("category-filter", "value"),
    )
    def update_trend_chart(selected_category):
        return trend_chart(df, selected_category)

    return dashboard
