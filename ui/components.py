"""UI components for member display."""

from typing import Optional


def render_status_badge(status: str, label: Optional[str] = None) -> str:
    """Render HTML status badge. Returns HTML string."""
    status_styles = {
        'active': ('Active', '#2ecc71', 'white'),
        'at_risk': ('At Risk', '#f1c40f', '#333'),
        'inactive': ('Inactive', '#e67e22', 'white'),
        'churned': ('Churned', '#e74c3c', 'white'),
        'unknown': ('Unknown', '#95a5a6', 'white'),
    }
    
    display_label, bg_color, text_color = status_styles.get(
        status.lower(), 
        ('Unknown', '#95a5a6', 'white')
    )
    
    if label:
        display_label = label
    
    return f"""
    <span style="
        display: inline-block;
        padding: 4px 12px;
        border-radius: 12px;
        background: {bg_color};
        color: {text_color};
        font-family: 'Cinzel', serif;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    ">{display_label}</span>
    """


def render_member_card(
    username: str,
    role: str,
    status: str,
    days_inactive: int,
    total_xp: float,
    ehp: float,
    ehb: float
) -> str:
    """Render member card HTML."""
    from utils import format_xp, format_hours, role_display_name
    
    status_colors = {
        'active': '#2ecc71',
        'at_risk': '#f1c40f',
        'inactive': '#e67e22',
        'churned': '#e74c3c',
        'unknown': '#95a5a6',
    }
    
    border_color = status_colors.get(status, '#95a5a6')
    
    activity_text = f"{days_inactive}d ago" if days_inactive >= 0 else "Never"
    
    return f"""
    <div style="
        background: linear-gradient(145deg, #8b7355 0%, #5c4d3a 100%);
        border: 2px solid {border_color};
        border-radius: 10px;
        padding: 12px 16px;
        margin: 6px 0;
        display: flex;
        align-items: center;
        justify-content: space-between;
    ">
        <div style="flex: 1;">
            <div style="
                color: #f4e4bc;
                font-family: 'Cinzel', serif;
                font-size: 1rem;
                font-weight: 600;
                margin-bottom: 4px;
            ">{username}</div>
            <div style="
                color: #d4af37;
                font-family: 'Crimson Text', serif;
                font-size: 0.8rem;
            ">{role_display_name(role)}</div>
        </div>
        <div style="text-align: right;">
            <div style="
                color: #f4e4bc;
                font-family: 'Crimson Text', serif;
                font-size: 0.9rem;
            ">{format_xp(total_xp)} XP</div>
            <div style="
                color: #a08b6d;
                font-family: 'Crimson Text', serif;
                font-size: 0.75rem;
            ">Last active: {activity_text}</div>
        </div>
        <div style="margin-left: 12px;">
            {render_status_badge(status)}
        </div>
    </div>
    """


def render_stat_card(title: str, value: str, subtitle: Optional[str] = None) -> str:
    """Render a stat display card."""
    subtitle_html = ""
    if subtitle:
        subtitle_html = f"""
        <div style="
            color: #a08b6d;
            font-family: 'Crimson Text', serif;
            font-size: 0.75rem;
            margin-top: 4px;
        ">{subtitle}</div>
        """
    
    return f"""
    <div style="
        background: linear-gradient(145deg, #8b7355 0%, #5c4d3a 100%);
        border: 2px solid #d4af37;
        border-radius: 10px;
        padding: 15px;
        text-align: center;
    ">
        <div style="
            color: #ffd700;
            font-family: 'Cinzel', serif;
            font-size: 0.85rem;
            margin-bottom: 8px;
        ">{title}</div>
        <div style="
            color: #f4e4bc;
            font-family: 'Crimson Text', serif;
            font-size: 1.4rem;
            font-weight: 600;
        ">{value}</div>
        {subtitle_html}
    </div>
    """


def render_health_score_display(score: float) -> str:
    """Render clan health score as circular gauge."""
    if score >= 70:
        color = '#2ecc71'
        label = 'Healthy'
    elif score >= 50:
        color = '#f1c40f'
        label = 'Moderate'
    elif score >= 30:
        color = '#e67e22'
        label = 'Concerning'
    else:
        color = '#e74c3c'
        label = 'Critical'
    
    return f"""
    <div style="
        background: linear-gradient(145deg, #8b7355 0%, #5c4d3a 100%);
        border: 4px solid {color};
        border-radius: 50%;
        width: 140px;
        height: 140px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        margin: 0 auto;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3), inset 0 2px 4px rgba(255,255,255,0.1);
    ">
        <div style="
            font-family: 'Cinzel', serif;
            font-size: 2.2rem;
            color: {color};
            font-weight: 700;
            line-height: 1;
        ">{score:.0f}</div>
        <div style="
            font-family: 'Crimson Text', serif;
            font-size: 0.85rem;
            color: #f4e4bc;
            margin-top: 4px;
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
    
    urgency_color = '#e74c3c' if days_inactive > 45 else '#e67e22' if days_inactive > 30 else '#f1c40f'
    
    return f"""
    <div style="
        background: linear-gradient(145deg, rgba(241,196,15,0.15) 0%, rgba(230,126,34,0.15) 100%);
        border: 2px solid {urgency_color};
        border-left: 6px solid {urgency_color};
        border-radius: 8px;
        padding: 12px 16px;
        margin: 6px 0;
    ">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div style="
                    color: #f4e4bc;
                    font-family: 'Cinzel', serif;
                    font-size: 0.95rem;
                    font-weight: 600;
                ">{username}</div>
                <div style="
                    color: #a08b6d;
                    font-family: 'Crimson Text', serif;
                    font-size: 0.75rem;
                ">{role_display_name(role)} • {format_xp(total_xp)} XP</div>
            </div>
            <div style="
                background: {urgency_color};
                color: white;
                padding: 6px 12px;
                border-radius: 15px;
                font-family: 'Cinzel', serif;
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
        background: linear-gradient(145deg, rgba(46,204,113,0.15) 0%, rgba(39,174,96,0.15) 100%);
        border: 2px solid #2ecc71;
        border-radius: 8px;
        padding: 10px 14px;
        margin: 4px 0;
    ">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div style="
                    color: #2ecc71;
                    font-family: 'Cinzel', serif;
                    font-size: 0.85rem;
                    font-weight: 600;
                ">{achievement_name}</div>
                <div style="
                    color: #f4e4bc;
                    font-family: 'Crimson Text', serif;
                    font-size: 0.8rem;
                ">{player_name}</div>
            </div>
            <div style="
                color: #a08b6d;
                font-family: 'Crimson Text', serif;
                font-size: 0.7rem;
                text-align: right;
            ">{created_at}</div>
        </div>
    </div>
    """
