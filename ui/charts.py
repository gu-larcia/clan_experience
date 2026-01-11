"""Modern Plotly charts for clan analytics."""

from typing import Dict, List, Optional
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Modern chart color scheme
CHART_COLORS = {
    'primary': '#3b82f6',
    'secondary': '#8b5cf6',
    'accent': '#06b6d4',
    'text': '#f8fafc',
    'text_secondary': '#94a3b8',
    'bg': '#1e293b',
    'bg_light': '#334155',
    'border': '#475569',
    'active': '#10b981',
    'at_risk': '#f59e0b',
    'inactive': '#f97316',
    'churned': '#ef4444',
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
            hole=0.6,
            textinfo='label+percent',
            textposition='outside',
            textfont=dict(color=CHART_COLORS['text'], size=12, family='Inter'),
            marker=dict(
                colors=colors,
                line=dict(color=CHART_COLORS['bg'], width=2)
            ),
            hovertemplate='<b>%{label}</b><br>Members: %{value}<br>Share: %{percent}<extra></extra>'
        )
    ])
    
    total = sum(values)
    fig.add_annotation(
        text=f"<b>{total}</b><br><span style='font-size:12px'>Members</span>",
        x=0.5, y=0.5,
        font=dict(color=CHART_COLORS['text'], size=24, family='Inter'),
        showarrow=False
    )
    
    fig.update_layout(
        title=dict(
            text="Activity Distribution",
            font=dict(color=CHART_COLORS['text'], size=16, family='Inter'),
            x=0.5,
        ),
        height=380,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        margin=dict(l=20, r=20, t=60, b=20),
    )
    
    return fig


def create_activity_timeline(timeline_data: List[Dict]) -> go.Figure:
    """Create bar chart showing member distribution by inactivity period."""
    buckets = [d['bucket'] for d in timeline_data]
    counts = [d['count'] for d in timeline_data]
    
    # Color gradient from green to red
    gradient = [
        CHART_COLORS['active'],
        '#22c55e',
        CHART_COLORS['at_risk'],
        '#fb923c',
        CHART_COLORS['inactive'],
        '#dc2626',
        CHART_COLORS['churned'],
        '#991b1b',
    ][:len(buckets)]
    
    fig = go.Figure(data=[
        go.Bar(
            x=buckets,
            y=counts,
            marker_color=gradient,
            marker_line_color=CHART_COLORS['bg'],
            marker_line_width=1,
            text=counts,
            textposition='outside',
            textfont=dict(color=CHART_COLORS['text'], size=11, family='Inter'),
            hovertemplate='<b>%{x}</b><br>Members: %{y}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=dict(
            text="Members by Last Activity",
            font=dict(color=CHART_COLORS['text'], size=16, family='Inter'),
            x=0.5,
        ),
        xaxis=dict(
            title="",
            tickfont=dict(color=CHART_COLORS['text_secondary'], size=10, family='Inter'),
            tickangle=45,
            gridcolor='rgba(71,85,105,0.3)',
        ),
        yaxis=dict(
            title="Member Count",
            title_font=dict(color=CHART_COLORS['text_secondary'], size=11, family='Inter'),
            tickfont=dict(color=CHART_COLORS['text_secondary'], size=10, family='Inter'),
            gridcolor='rgba(71,85,105,0.3)',
        ),
        height=380,
        margin=dict(l=50, r=20, t=60, b=100),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
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
            marker_color=CHART_COLORS['primary'],
            marker_line_color=CHART_COLORS['bg'],
            marker_line_width=1,
            text=[format_xp(g) for g in gains],
            textposition='outside',
            textfont=dict(color=CHART_COLORS['text'], size=11, family='Inter'),
            hovertemplate='<b>%{y}</b><br>XP Gained: %{x:,.0f}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=dict(
            text=f"Top {metric.title()} XP Gainers",
            font=dict(color=CHART_COLORS['text'], size=16, family='Inter'),
            x=0.5,
        ),
        xaxis=dict(
            title="XP Gained",
            title_font=dict(color=CHART_COLORS['text_secondary'], size=11, family='Inter'),
            tickfont=dict(color=CHART_COLORS['text_secondary'], size=10, family='Inter'),
            gridcolor='rgba(71,85,105,0.3)',
            tickformat=',.0f',
        ),
        yaxis=dict(
            title="",
            tickfont=dict(color=CHART_COLORS['text'], size=11, family='Inter'),
            autorange="reversed",
        ),
        height=max(400, len(sorted_data) * 32),
        margin=dict(l=120, r=80, t=60, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    
    return fig


def create_role_distribution(role_counts: Dict[str, int]) -> go.Figure:
    """Create horizontal bar chart of member roles."""
    # Sort by count
    sorted_roles = sorted(role_counts.items(), key=lambda x: x[1], reverse=True)[:12]
    
    labels = [r[0].replace('_', ' ').title() for r in sorted_roles]
    values = [r[1] for r in sorted_roles]
    
    fig = go.Figure(data=[
        go.Bar(
            x=values,
            y=labels,
            orientation='h',
            marker_color=CHART_COLORS['secondary'],
            marker_line_color=CHART_COLORS['bg'],
            marker_line_width=1,
            text=values,
            textposition='outside',
            textfont=dict(color=CHART_COLORS['text'], size=11, family='Inter'),
            hovertemplate='<b>%{y}</b><br>Members: %{x}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=dict(
            text="Member Roles",
            font=dict(color=CHART_COLORS['text'], size=16, family='Inter'),
            x=0.5,
        ),
        xaxis=dict(
            title="Count",
            title_font=dict(color=CHART_COLORS['text_secondary'], size=11, family='Inter'),
            tickfont=dict(color=CHART_COLORS['text_secondary'], size=10, family='Inter'),
            gridcolor='rgba(71,85,105,0.3)',
        ),
        yaxis=dict(
            title="",
            tickfont=dict(color=CHART_COLORS['text'], size=11, family='Inter'),
            autorange="reversed",
        ),
        height=max(300, len(sorted_roles) * 30),
        margin=dict(l=120, r=60, t=60, b=40),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    
    return fig


def create_retention_chart(retention_rates: Dict[int, float]) -> go.Figure:
    """Create line chart showing retention at different day thresholds."""
    days = list(retention_rates.keys())
    rates = list(retention_rates.values())
    
    fig = go.Figure()
    
    # Add gradient fill
    fig.add_trace(go.Scatter(
        x=days,
        y=rates,
        mode='lines',
        fill='tozeroy',
        line=dict(color=CHART_COLORS['primary'], width=3),
        fillcolor='rgba(59, 130, 246, 0.2)',
        hovertemplate='<b>Day %{x}</b><br>Retention: %{y:.1f}%<extra></extra>'
    ))
    
    # Add markers
    fig.add_trace(go.Scatter(
        x=days,
        y=rates,
        mode='markers+text',
        marker=dict(size=12, color=CHART_COLORS['primary'], line=dict(width=2, color='white')),
        text=[f"{r:.0f}%" for r in rates],
        textposition='top center',
        textfont=dict(color=CHART_COLORS['text'], size=12, family='Inter'),
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Add 50% benchmark line
    fig.add_hline(
        y=50, 
        line_dash="dash", 
        line_color="rgba(148, 163, 184, 0.5)",
        annotation_text="50% benchmark",
        annotation_position="right",
        annotation_font=dict(color=CHART_COLORS['text_secondary'], size=10, family='Inter')
    )
    
    fig.update_layout(
        title=dict(
            text="Retention Rate by Day",
            font=dict(color=CHART_COLORS['text'], size=16, family='Inter'),
            x=0.5,
        ),
        xaxis=dict(
            title="Days Since Last Activity",
            title_font=dict(color=CHART_COLORS['text_secondary'], size=11, family='Inter'),
            tickfont=dict(color=CHART_COLORS['text_secondary'], size=10, family='Inter'),
            gridcolor='rgba(71,85,105,0.3)',
            tickmode='array',
            tickvals=days,
        ),
        yaxis=dict(
            title="Retention %",
            title_font=dict(color=CHART_COLORS['text_secondary'], size=11, family='Inter'),
            tickfont=dict(color=CHART_COLORS['text_secondary'], size=10, family='Inter'),
            gridcolor='rgba(71,85,105,0.3)',
            range=[0, 105],
        ),
        height=380,
        margin=dict(l=50, r=50, t=60, b=50),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
    )
    
    return fig


def create_xp_distribution(members: List[Dict]) -> go.Figure:
    """Create histogram of total XP distribution."""
    xp_values = [m.get('exp', 0) or 0 for m in members]
    
    fig = go.Figure(data=[
        go.Histogram(
            x=xp_values,
            nbinsx=20,
            marker_color=CHART_COLORS['accent'],
            marker_line_color=CHART_COLORS['bg'],
            marker_line_width=1,
            hovertemplate='XP Range: %{x}<br>Members: %{y}<extra></extra>'
        )
    ])
    
    fig.update_layout(
        title=dict(
            text="Total XP Distribution",
            font=dict(color=CHART_COLORS['text'], size=16, family='Inter'),
            x=0.5,
        ),
        xaxis=dict(
            title="Total XP",
            title_font=dict(color=CHART_COLORS['text_secondary'], size=11, family='Inter'),
            tickfont=dict(color=CHART_COLORS['text_secondary'], size=10, family='Inter'),
            gridcolor='rgba(71,85,105,0.3)',
            tickformat=',.0f',
        ),
        yaxis=dict(
            title="Member Count",
            title_font=dict(color=CHART_COLORS['text_secondary'], size=11, family='Inter'),
            tickfont=dict(color=CHART_COLORS['text_secondary'], size=10, family='Inter'),
            gridcolor='rgba(71,85,105,0.3)',
        ),
        height=340,
        margin=dict(l=50, r=20, t=60, b=50),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
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
        'unknown': '#6b7280',
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
                    line=dict(width=1, color=CHART_COLORS['bg']),
                    opacity=0.8
                ),
                text=[m.get('username', 'Unknown') for m in status_members],
                hovertemplate='<b>%{text}</b><br>EHP: %{x:.1f}<br>EHB: %{y:.1f}<extra></extra>'
            ))
    
    fig.update_layout(
        title=dict(
            text="EHP vs EHB",
            font=dict(color=CHART_COLORS['text'], size=16, family='Inter'),
            x=0.5,
        ),
        xaxis=dict(
            title="Efficient Hours Played (EHP)",
            title_font=dict(color=CHART_COLORS['text_secondary'], size=11, family='Inter'),
            tickfont=dict(color=CHART_COLORS['text_secondary'], size=10, family='Inter'),
            gridcolor='rgba(71,85,105,0.3)',
        ),
        yaxis=dict(
            title="Efficient Hours Bossed (EHB)",
            title_font=dict(color=CHART_COLORS['text_secondary'], size=11, family='Inter'),
            tickfont=dict(color=CHART_COLORS['text_secondary'], size=10, family='Inter'),
            gridcolor='rgba(71,85,105,0.3)',
        ),
        height=400,
        margin=dict(l=50, r=20, t=60, b=50),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(
            font=dict(color=CHART_COLORS['text'], size=11, family='Inter'),
            bgcolor='rgba(30,41,59,0.8)',
            bordercolor=CHART_COLORS['border'],
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
            font=dict(color=CHART_COLORS['text'], size=48, family='Inter'),
            suffix=""
        ),
        gauge=dict(
            axis=dict(
                range=[0, 100],
                tickfont=dict(color=CHART_COLORS['text_secondary'], size=10, family='Inter'),
                tickcolor=CHART_COLORS['text_secondary'],
            ),
            bar=dict(color=color, thickness=0.8),
            bgcolor=CHART_COLORS['bg_light'],
            bordercolor=CHART_COLORS['border'],
            borderwidth=2,
            steps=[
                dict(range=[0, 30], color='rgba(239,68,68,0.15)'),
                dict(range=[30, 50], color='rgba(249,115,22,0.15)'),
                dict(range=[50, 70], color='rgba(245,158,11,0.15)'),
                dict(range=[70, 100], color='rgba(16,185,129,0.15)'),
            ],
        )
    ))
    
    fig.update_layout(
        height=280,
        margin=dict(l=30, r=30, t=30, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
    )
    
    return fig
