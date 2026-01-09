"""Plotly chart functions for clan analytics."""

from typing import Dict, List, Optional
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Chart color scheme
CHART_COLORS = {
    'gold': '#d4af37',
    'gold_dark': '#b8860b',
    'parchment': '#f4e4bc',
    'ocean_dark': '#1a2a3a',
    'driftwood': '#8b7355',
    'rune_blue': '#5dade2',
    'active': '#2ecc71',
    'at_risk': '#f1c40f',
    'inactive': '#e67e22',
    'churned': '#e74c3c',
}


def create_activity_donut(status_counts: Dict[str, int]) -> go.Figure:
    """Create donut chart showing activity distribution."""
    labels = []
    values = []
    colors = []
    
    status_config = {
        'active': ('Active', CHART_COLORS['active']),
        'at_risk': ('At Risk', CHART_COLORS['at_risk']),
        'inactive': ('Inactive', CHART_COLORS['inactive']),
        'churned': ('Churned', CHART_COLORS['churned']),
    }
    
    for status, (label, color) in status_config.items():
        if status_counts.get(status, 0) > 0:
            labels.append(label)
            values.append(status_counts[status])
            colors.append(color)
    
    fig = go.Figure(data=[
        go.Pie(
            labels=labels,
            values=values,
            hole=0.5,
            textinfo='label+percent',
            textposition='outside',
            textfont=dict(color=CHART_COLORS['parchment'], size=11),
            marker=dict(
                colors=colors,
                line=dict(color=CHART_COLORS['ocean_dark'], width=2)
            ),
            hovertemplate='<b>%{label}</b><br>Members: %{value}<br>Share: %{percent}<extra></extra>'
        )
    ])
    
    total = sum(values)
    fig.add_annotation(
        text=f"<b>{total}</b><br>Members",
        x=0.5, y=0.5,
        font=dict(color=CHART_COLORS['gold'], size=16),
        showarrow=False
    )
    
    fig.update_layout(
        title=dict(
            text="Activity Distribution",
            font=dict(color=CHART_COLORS['gold'], size=16)
        ),
        height=350,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,42,58,0.8)',
        showlegend=False,
        margin=dict(l=20, r=20, t=50, b=20),
    )
    
    return fig


def create_activity_timeline(timeline_data: List[Dict]) -> go.Figure:
    """Create bar chart showing member distribution by inactivity period."""
    buckets = [d['bucket'] for d in timeline_data]
    counts = [d['count'] for d in timeline_data]
    
    # Color gradient from green to red
    colors = [
        CHART_COLORS['active'],
        '#27ae60',
        CHART_COLORS['at_risk'],
        '#e67e22',
        CHART_COLORS['inactive'],
        '#c0392b',
        CHART_COLORS['churned'],
        '#922b21',
    ][:len(buckets)]
    
    fig = go.Figure(data=[
        go.Bar(
            x=buckets,
            y=counts,
            marker_color=colors,
            marker_line_color=CHART_COLORS['ocean_dark'],
            marker_line_width=1.5,
            text=counts,
            textposition='outside',
            textfont=dict(color=CHART_COLORS['parchment'], size=10),
            hovertemplate='<b>%{x}</b><br>Members: %{y}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=dict(
            text="Members by Last Activity",
            font=dict(color=CHART_COLORS['gold'], size=16)
        ),
        xaxis=dict(
            title="Days Since Last Activity",
            title_font=dict(color=CHART_COLORS['parchment'], size=11),
            tickfont=dict(color=CHART_COLORS['parchment'], size=9),
            tickangle=45,
        ),
        yaxis=dict(
            title="Member Count",
            title_font=dict(color=CHART_COLORS['parchment'], size=11),
            tickfont=dict(color=CHART_COLORS['parchment'], size=9),
            gridcolor='rgba(139,115,85,0.25)',
        ),
        height=350,
        margin=dict(l=50, r=20, t=50, b=80),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,42,58,0.8)',
    )
    
    return fig


def create_xp_gains_chart(gains_data: List[Dict], metric: str = "overall") -> go.Figure:
    """Create horizontal bar chart of top XP gainers."""
    # Sort by gained XP
    sorted_data = sorted(gains_data, key=lambda x: x.get('data', {}).get('gained', 0), reverse=True)[:15]
    
    usernames = [d.get('player', {}).get('displayName', 'Unknown') for d in sorted_data]
    gains = [d.get('data', {}).get('gained', 0) for d in sorted_data]
    
    # Format XP values for display
    def format_xp(val):
        if val >= 1_000_000:
            return f"{val/1_000_000:.1f}M"
        elif val >= 1_000:
            return f"{val/1_000:.0f}K"
        return str(int(val))
    
    fig = go.Figure(data=[
        go.Bar(
            x=gains,
            y=usernames,
            orientation='h',
            marker_color=CHART_COLORS['gold'],
            marker_line_color=CHART_COLORS['gold_dark'],
            marker_line_width=1.5,
            text=[format_xp(g) for g in gains],
            textposition='outside',
            textfont=dict(color=CHART_COLORS['parchment'], size=10),
            hovertemplate='<b>%{y}</b><br>XP Gained: %{x:,.0f}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=dict(
            text=f"Top {metric.title()} XP Gainers",
            font=dict(color=CHART_COLORS['gold'], size=16)
        ),
        xaxis=dict(
            title="XP Gained",
            title_font=dict(color=CHART_COLORS['parchment'], size=11),
            tickfont=dict(color=CHART_COLORS['parchment'], size=9),
            gridcolor='rgba(139,115,85,0.25)',
            tickformat=',.0f',
        ),
        yaxis=dict(
            title="",
            tickfont=dict(color=CHART_COLORS['parchment'], size=10),
            autorange="reversed",
        ),
        height=max(400, len(sorted_data) * 28),
        margin=dict(l=120, r=80, t=50, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,42,58,0.8)',
    )
    
    return fig


def create_role_distribution(role_counts: Dict[str, int]) -> go.Figure:
    """Create pie chart of member roles."""
    # Sort by count and take top roles
    sorted_roles = sorted(role_counts.items(), key=lambda x: x[1], reverse=True)
    
    labels = [r[0].replace('_', ' ').title() for r in sorted_roles[:10]]
    values = [r[1] for r in sorted_roles[:10]]
    
    # Generate colors
    colors = px.colors.qualitative.Set2[:len(labels)]
    
    fig = go.Figure(data=[
        go.Pie(
            labels=labels,
            values=values,
            textinfo='label+value',
            textposition='outside',
            textfont=dict(color=CHART_COLORS['parchment'], size=10),
            marker=dict(
                colors=colors,
                line=dict(color=CHART_COLORS['ocean_dark'], width=1.5)
            ),
            hovertemplate='<b>%{label}</b><br>Members: %{value}<br>Share: %{percent}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=dict(
            text="Member Roles",
            font=dict(color=CHART_COLORS['gold'], size=16)
        ),
        height=350,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,42,58,0.8)',
        showlegend=False,
        margin=dict(l=20, r=20, t=50, b=20),
    )
    
    return fig


def create_retention_chart(retention_rates: Dict[int, float]) -> go.Figure:
    """Create line chart showing retention at different day thresholds."""
    days = list(retention_rates.keys())
    rates = list(retention_rates.values())
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=days,
        y=rates,
        mode='lines+markers+text',
        line=dict(color=CHART_COLORS['gold'], width=3),
        marker=dict(size=12, color=CHART_COLORS['gold'], line=dict(width=2, color=CHART_COLORS['gold_dark'])),
        text=[f"{r:.0f}%" for r in rates],
        textposition='top center',
        textfont=dict(color=CHART_COLORS['parchment'], size=11),
        hovertemplate='<b>Day %{x}</b><br>Retention: %{y:.1f}%<extra></extra>'
    ))
    
    # Add benchmark line at 50%
    fig.add_hline(
        y=50, 
        line_dash="dash", 
        line_color="rgba(244,228,188,0.4)",
        annotation_text="50% benchmark",
        annotation_position="right",
        annotation_font=dict(color=CHART_COLORS['parchment'], size=10)
    )
    
    fig.update_layout(
        title=dict(
            text="Retention Rate by Day",
            font=dict(color=CHART_COLORS['gold'], size=16),
            subtitle=dict(
                text="% of members active within N days",
                font=dict(color='#a08b6d', size=10)
            )
        ),
        xaxis=dict(
            title="Days",
            title_font=dict(color=CHART_COLORS['parchment'], size=11),
            tickfont=dict(color=CHART_COLORS['parchment'], size=10),
            gridcolor='rgba(139,115,85,0.25)',
            tickmode='array',
            tickvals=days,
        ),
        yaxis=dict(
            title="Retention %",
            title_font=dict(color=CHART_COLORS['parchment'], size=11),
            tickfont=dict(color=CHART_COLORS['parchment'], size=10),
            gridcolor='rgba(139,115,85,0.25)',
            range=[0, 105],
        ),
        height=350,
        margin=dict(l=50, r=50, t=60, b=50),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,42,58,0.8)',
    )
    
    return fig


def create_xp_distribution(members: List[Dict]) -> go.Figure:
    """Create histogram of total XP distribution."""
    xp_values = [m.get('exp', 0) or 0 for m in members]
    
    fig = go.Figure(data=[
        go.Histogram(
            x=xp_values,
            nbinsx=20,
            marker_color=CHART_COLORS['gold'],
            marker_line_color=CHART_COLORS['gold_dark'],
            marker_line_width=1,
            hovertemplate='XP Range: %{x}<br>Members: %{y}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=dict(
            text="Total XP Distribution",
            font=dict(color=CHART_COLORS['gold'], size=16)
        ),
        xaxis=dict(
            title="Total XP",
            title_font=dict(color=CHART_COLORS['parchment'], size=11),
            tickfont=dict(color=CHART_COLORS['parchment'], size=9),
            gridcolor='rgba(139,115,85,0.25)',
            tickformat=',.0f',
        ),
        yaxis=dict(
            title="Member Count",
            title_font=dict(color=CHART_COLORS['parchment'], size=11),
            tickfont=dict(color=CHART_COLORS['parchment'], size=9),
            gridcolor='rgba(139,115,85,0.25)',
        ),
        height=300,
        margin=dict(l=50, r=20, t=50, b=50),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,42,58,0.8)',
    )
    
    return fig


def create_ehp_vs_ehb_scatter(members: List[Dict]) -> go.Figure:
    """Create scatter plot of EHP vs EHB."""
    fig = go.Figure()
    
    # Color by activity status
    status_colors = {
        'active': CHART_COLORS['active'],
        'at_risk': CHART_COLORS['at_risk'],
        'inactive': CHART_COLORS['inactive'],
        'churned': CHART_COLORS['churned'],
        'unknown': '#95a5a6',
    }
    
    for status, color in status_colors.items():
        status_members = [m for m in members if m.get('activity_status') == status]
        if status_members:
            fig.add_trace(go.Scatter(
                x=[m.get('ehp', 0) or 0 for m in status_members],
                y=[m.get('ehb', 0) or 0 for m in status_members],
                mode='markers',
                name=status.replace('_', ' ').title(),
                marker=dict(
                    size=10,
                    color=color,
                    line=dict(width=1, color=CHART_COLORS['ocean_dark'])
                ),
                text=[m.get('username', 'Unknown') for m in status_members],
                hovertemplate='<b>%{text}</b><br>EHP: %{x:.1f}<br>EHB: %{y:.1f}<extra></extra>'
            ))
    
    fig.update_layout(
        title=dict(
            text="EHP vs EHB",
            font=dict(color=CHART_COLORS['gold'], size=16),
            subtitle=dict(
                text="Skilling vs Bossing efficiency",
                font=dict(color='#a08b6d', size=10)
            )
        ),
        xaxis=dict(
            title="Efficient Hours Played (EHP)",
            title_font=dict(color=CHART_COLORS['parchment'], size=11),
            tickfont=dict(color=CHART_COLORS['parchment'], size=9),
            gridcolor='rgba(139,115,85,0.25)',
        ),
        yaxis=dict(
            title="Efficient Hours Bossed (EHB)",
            title_font=dict(color=CHART_COLORS['parchment'], size=11),
            tickfont=dict(color=CHART_COLORS['parchment'], size=9),
            gridcolor='rgba(139,115,85,0.25)',
        ),
        height=400,
        margin=dict(l=50, r=20, t=60, b=50),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(26,42,58,0.8)',
        legend=dict(
            font=dict(color=CHART_COLORS['parchment'], size=10),
            bgcolor='rgba(26,42,58,0.8)',
            bordercolor=CHART_COLORS['driftwood'],
            borderwidth=1,
        )
    )
    
    return fig


def create_health_gauge(score: float) -> go.Figure:
    """Create gauge chart for clan health score."""
    # Determine color based on score
    if score >= 70:
        color = CHART_COLORS['active']
    elif score >= 50:
        color = CHART_COLORS['at_risk']
    elif score >= 30:
        color = CHART_COLORS['inactive']
    else:
        color = CHART_COLORS['churned']
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        domain={'x': [0, 1], 'y': [0, 1]},
        number=dict(
            font=dict(color=CHART_COLORS['gold'], size=40),
            suffix=""
        ),
        gauge=dict(
            axis=dict(
                range=[0, 100],
                tickfont=dict(color=CHART_COLORS['parchment'], size=10),
                tickcolor=CHART_COLORS['parchment'],
            ),
            bar=dict(color=color, thickness=0.75),
            bgcolor=CHART_COLORS['ocean_dark'],
            bordercolor=CHART_COLORS['gold_dark'],
            borderwidth=2,
            steps=[
                dict(range=[0, 30], color='rgba(231,76,60,0.3)'),
                dict(range=[30, 50], color='rgba(230,126,34,0.3)'),
                dict(range=[50, 70], color='rgba(241,196,15,0.3)'),
                dict(range=[70, 100], color='rgba(46,204,113,0.3)'),
            ],
        )
    ))
    
    fig.update_layout(
        title=dict(
            text="Clan Health Score",
            font=dict(color=CHART_COLORS['gold'], size=16),
            y=0.85,
        ),
        height=250,
        margin=dict(l=30, r=30, t=80, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    return fig
