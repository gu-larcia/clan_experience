"""Modern UI components for clan analytics."""

from typing import Optional


def render_status_badge(status: str, label: Optional[str] = None) -> str:
    """Render HTML status badge. Returns HTML string."""
    status_styles = {
        'active': ('Active', '#10b981', 'rgba(16,185,129,0.15)'),
        'at_risk': ('At Risk', '#f59e0b', 'rgba(245,158,11,0.15)'),
        'inactive': ('Inactive', '#f97316', 'rgba(249,115,22,0.15)'),
        'churned': ('Churned', '#ef4444', 'rgba(239,68,68,0.15)'),
        'unknown': ('Unknown', '#6b7280', 'rgba(107,114,128,0.15)'),
    }
    
    display_label, text_color, bg_color = status_styles.get(
        status.lower(), 
        ('Unknown', '#6b7280', 'rgba(107,114,128,0.15)')
    )
    
    if label:
        display_label = label
    
    return f"""
    <span style="
        display: inline-flex;
        align-items: center;
        padding: 4px 12px;
        border-radius: 9999px;
        background: {bg_color};
        color: {text_color};
        font-family: 'Inter', -apple-system, sans-serif;
        font-size: 0.75rem;
        font-weight: 500;
    ">{display_label}</span>
    """


def render_stat_card(title: str, value: str, subtitle: Optional[str] = None, color: str = "#3b82f6") -> str:
    """Render a stat display card."""
    subtitle_html = ""
    if subtitle:
        subtitle_html = f"""
        <div style="
            color: #64748b;
            font-family: 'Inter', -apple-system, sans-serif;
            font-size: 0.75rem;
            margin-top: 4px;
        ">{subtitle}</div>
        """
    
    return f"""
    <div style="
        background: #1e293b;
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    ">
        <div style="
            color: #94a3b8;
            font-family: 'Inter', -apple-system, sans-serif;
            font-size: 0.75rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 8px;
        ">{title}</div>
        <div style="
            color: {color};
            font-family: 'Inter', -apple-system, sans-serif;
            font-size: 1.5rem;
            font-weight: 700;
        ">{value}</div>
        {subtitle_html}
    </div>
    """


def render_health_score_display(score: float) -> str:
    """Render clan health score as circular display."""
    if score >= 70:
        color = '#10b981'
        label = 'Healthy'
        bg = 'rgba(16,185,129,0.15)'
    elif score >= 50:
        color = '#f59e0b'
        label = 'Moderate'
        bg = 'rgba(245,158,11,0.15)'
    elif score >= 30:
        color = '#f97316'
        label = 'Concerning'
        bg = 'rgba(249,115,22,0.15)'
    else:
        color = '#ef4444'
        label = 'Critical'
        bg = 'rgba(239,68,68,0.15)'
    
    return f"""
    <div style="
        background: {bg};
        border: 3px solid {color};
        border-radius: 50%;
        width: 160px;
        height: 160px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 0 auto;
    ">
        <div style="
            font-family: 'Inter', -apple-system, sans-serif;
            font-size: 2.5rem;
            color: {color};
            font-weight: 700;
            line-height: 1;
        ">{score:.0f}</div>
        <div style="
            font-family: 'Inter', -apple-system, sans-serif;
            font-size: 0.875rem;
            color: #94a3b8;
            margin-top: 4px;
            font-weight: 500;
        ">{label}</div>
    </div>
    """


def render_at_risk_card(
    username: str,
    days_inactive: int,
    total_xp: float,
    role: str
) -> str:
    """Render at-risk member card with warning styling."""
    from utils import format_xp, role_display_name
    
    if days_inactive > 45:
        urgency_color = '#ef4444'
        urgency_bg = 'rgba(239,68,68,0.1)'
    elif days_inactive > 30:
        urgency_color = '#f97316'
        urgency_bg = 'rgba(249,115,22,0.1)'
    else:
        urgency_color = '#f59e0b'
        urgency_bg = 'rgba(245,158,11,0.1)'
    
    return f"""
    <div style="
        background: {urgency_bg};
        border: 1px solid {urgency_color}33;
        border-left: 4px solid {urgency_color};
        border-radius: 8px;
        padding: 12px 16px;
        margin: 8px 0;
    ">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div style="
                    color: #f8fafc;
                    font-family: 'Inter', -apple-system, sans-serif;
                    font-size: 0.95rem;
                    font-weight: 600;
                ">{username}</div>
                <div style="
                    color: #94a3b8;
                    font-family: 'Inter', -apple-system, sans-serif;
                    font-size: 0.75rem;
                    margin-top: 2px;
                ">{role_display_name(role)} • {format_xp(total_xp)} XP</div>
            </div>
            <div style="
                background: {urgency_color};
                color: white;
                padding: 6px 12px;
                border-radius: 9999px;
                font-family: 'Inter', -apple-system, sans-serif;
                font-size: 0.75rem;
                font-weight: 600;
            ">{days_inactive} days</div>
        </div>
    </div>
    """


def render_achievement_card(
    player_name: str,
    achievement_name: str,
    metric: str,
    threshold: int,
    created_at: str
) -> str:
    """Render recent achievement card."""
    return f"""
    <div style="
        background: rgba(16,185,129,0.1);
        border: 1px solid rgba(16,185,129,0.3);
        border-radius: 8px;
        padding: 12px 16px;
        margin: 6px 0;
    ">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div style="
                    color: #10b981;
                    font-family: 'Inter', -apple-system, sans-serif;
                    font-size: 0.875rem;
                    font-weight: 600;
                ">{achievement_name}</div>
                <div style="
                    color: #f8fafc;
                    font-family: 'Inter', -apple-system, sans-serif;
                    font-size: 0.8rem;
                    margin-top: 2px;
                ">{player_name}</div>
            </div>
            <div style="
                color: #64748b;
                font-family: 'Inter', -apple-system, sans-serif;
                font-size: 0.7rem;
                text-align: right;
            ">{created_at}</div>
        </div>
    </div>
    """


def render_api_status(has_key: bool, member_count: int) -> str:
    """Render API status indicator."""
    if has_key:
        status_color = '#10b981'
        status_text = '100 req/min'
        icon = '✓'
    else:
        status_color = '#f59e0b'
        status_text = '20 req/min'
        icon = '!'
    
    return f"""
    <div style="
        display: flex;
        align-items: center;
        gap: 8px;
        padding: 8px 12px;
        background: rgba(30,41,59,0.8);
        border: 1px solid #334155;
        border-radius: 8px;
        font-family: 'Inter', -apple-system, sans-serif;
        font-size: 0.75rem;
    ">
        <span style="
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 18px;
            height: 18px;
            border-radius: 50%;
            background: {status_color}22;
            color: {status_color};
            font-weight: 600;
        ">{icon}</span>
        <span style="color: #94a3b8;">API Key:</span>
        <span style="color: {status_color}; font-weight: 500;">{status_text}</span>
        <span style="color: #475569;">|</span>
        <span style="color: #94a3b8;">{member_count} members loaded</span>
    </div>
    """
