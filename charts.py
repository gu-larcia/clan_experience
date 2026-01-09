"""Plotly chart builders."""

import plotly.graph_objects as go

# Color scheme
GOLD = "#d4af37"
PARCHMENT = "#f4e4bc"
DARK_BG = "rgba(26,42,58,0.8)"
GRID = "rgba(139,115,85,0.25)"

STATUS_COLORS = {
    "active": "#2ecc71",
    "at_risk": "#f1c40f",
    "inactive": "#e67e22",
    "churned": "#e74c3c",
}


def _base_layout(title: str, height: int = 350) -> dict:
    """Shared layout config."""
    return {
        "title": {"text": title, "font": {"color": GOLD, "size": 16}},
        "height": height,
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": DARK_BG,
        "margin": {"l": 50, "r": 30, "t": 50, "b": 50},
    }


def activity_donut(counts: dict[str, int]) -> go.Figure:
    """Donut chart of activity distribution."""
    labels, values, colors = [], [], []
    
    for status in ["active", "at_risk", "inactive", "churned"]:
        if counts.get(status, 0) > 0:
            labels.append(status.replace("_", " ").title())
            values.append(counts[status])
            colors.append(STATUS_COLORS[status])

    fig = go.Figure(go.Pie(
        labels=labels,
        values=values,
        hole=0.5,
        textinfo="label+percent",
        textposition="outside",
        textfont={"color": PARCHMENT, "size": 11},
        marker={"colors": colors, "line": {"color": DARK_BG, "width": 2}},
    ))

    total = sum(values)
    fig.add_annotation(
        text=f"<b>{total}</b><br>Members",
        x=0.5, y=0.5,
        font={"color": GOLD, "size": 16},
        showarrow=False,
    )

    layout = _base_layout("Activity Distribution")
    layout["showlegend"] = False
    fig.update_layout(**layout)
    
    return fig


def activity_bars(buckets: list[dict]) -> go.Figure:
    """Bar chart of members by inactivity period."""
    labels = [b["label"] for b in buckets]
    counts = [b["count"] for b in buckets]
    
    # Gradient from green to red
    colors = [
        "#2ecc71", "#27ae60", "#f1c40f", "#e67e22",
        "#e74c3c", "#c0392b", "#922b21", "#641e16",
    ][:len(labels)]

    fig = go.Figure(go.Bar(
        x=labels,
        y=counts,
        marker_color=colors,
        text=counts,
        textposition="outside",
        textfont={"color": PARCHMENT, "size": 10},
    ))

    layout = _base_layout("Members by Last Activity")
    layout["xaxis"] = {
        "title": "Days Since Activity",
        "tickfont": {"color": PARCHMENT, "size": 9},
        "tickangle": 45,
    }
    layout["yaxis"] = {
        "title": "Count",
        "tickfont": {"color": PARCHMENT},
        "gridcolor": GRID,
    }
    layout["margin"]["b"] = 80
    fig.update_layout(**layout)
    
    return fig


def xp_gainers(gains: list[dict], metric: str = "overall", limit: int = 15) -> go.Figure:
    """Horizontal bar chart of top XP gainers."""
    # Sort and limit
    sorted_gains = sorted(
        gains,
        key=lambda x: x.get("data", {}).get("gained", 0),
        reverse=True,
    )[:limit]

    names = [g.get("player", {}).get("displayName", "?") for g in sorted_gains]
    values = [g.get("data", {}).get("gained", 0) for g in sorted_gains]

    def fmt(v):
        if v >= 1_000_000:
            return f"{v/1_000_000:.1f}M"
        if v >= 1_000:
            return f"{v/1_000:.0f}K"
        return str(int(v))

    fig = go.Figure(go.Bar(
        x=values,
        y=names,
        orientation="h",
        marker_color=GOLD,
        text=[fmt(v) for v in values],
        textposition="outside",
        textfont={"color": PARCHMENT, "size": 10},
    ))

    layout = _base_layout(f"Top {metric.title()} Gainers", height=max(350, len(sorted_gains) * 28))
    layout["xaxis"] = {"title": "XP Gained", "tickfont": {"color": PARCHMENT}, "gridcolor": GRID}
    layout["yaxis"] = {"tickfont": {"color": PARCHMENT}, "autorange": "reversed"}
    layout["margin"]["l"] = 120
    layout["margin"]["r"] = 60
    fig.update_layout(**layout)
    
    return fig


def retention_line(rates: dict[int, float]) -> go.Figure:
    """Line chart of retention rates."""
    days = list(rates.keys())
    pcts = list(rates.values())

    fig = go.Figure(go.Scatter(
        x=days,
        y=pcts,
        mode="lines+markers+text",
        line={"color": GOLD, "width": 3},
        marker={"size": 12, "color": GOLD},
        text=[f"{p:.0f}%" for p in pcts],
        textposition="top center",
        textfont={"color": PARCHMENT, "size": 11},
    ))

    fig.add_hline(y=50, line_dash="dash", line_color="rgba(244,228,188,0.4)")

    layout = _base_layout("Retention by Day")
    layout["xaxis"] = {
        "title": "Days",
        "tickfont": {"color": PARCHMENT},
        "tickmode": "array",
        "tickvals": days,
        "gridcolor": GRID,
    }
    layout["yaxis"] = {
        "title": "% Active",
        "tickfont": {"color": PARCHMENT},
        "range": [0, 105],
        "gridcolor": GRID,
    }
    fig.update_layout(**layout)
    
    return fig


def health_gauge(score: float) -> go.Figure:
    """Gauge chart for clan health score."""
    if score >= 70:
        color = STATUS_COLORS["active"]
    elif score >= 50:
        color = STATUS_COLORS["at_risk"]
    elif score >= 30:
        color = STATUS_COLORS["inactive"]
    else:
        color = STATUS_COLORS["churned"]

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={"font": {"color": GOLD, "size": 36}},
        gauge={
            "axis": {"range": [0, 100], "tickfont": {"color": PARCHMENT}},
            "bar": {"color": color, "thickness": 0.75},
            "bgcolor": DARK_BG,
            "bordercolor": "#b8860b",
            "borderwidth": 2,
            "steps": [
                {"range": [0, 30], "color": "rgba(231,76,60,0.3)"},
                {"range": [30, 50], "color": "rgba(230,126,34,0.3)"},
                {"range": [50, 70], "color": "rgba(241,196,15,0.3)"},
                {"range": [70, 100], "color": "rgba(46,204,113,0.3)"},
            ],
        },
    ))

    layout = _base_layout("Clan Health", height=220)
    layout["margin"] = {"l": 30, "r": 30, "t": 60, "b": 20}
    fig.update_layout(**layout)
    
    return fig


def xp_histogram(members: list[dict]) -> go.Figure:
    """Histogram of total XP distribution."""
    xp_vals = [m.get("xp", 0) for m in members]

    fig = go.Figure(go.Histogram(
        x=xp_vals,
        nbinsx=20,
        marker_color=GOLD,
        marker_line_color="#b8860b",
        marker_line_width=1,
    ))

    layout = _base_layout("XP Distribution", height=300)
    layout["xaxis"] = {"title": "Total XP", "tickfont": {"color": PARCHMENT}, "gridcolor": GRID}
    layout["yaxis"] = {"title": "Members", "tickfont": {"color": PARCHMENT}, "gridcolor": GRID}
    fig.update_layout(**layout)
    
    return fig
