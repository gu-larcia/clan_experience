"""UI components for clan analytics display."""

from typing import Optional


def render_status_badge(status: str, label: Optional[str] = None) -> str:
    """Render HTML status badge."""
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

    return (
        f'<span style="display:inline-flex;align-items:center;padding:4px 12px;'
        f'border-radius:9999px;background:{bg_color};color:{text_color};'
        f"font-family:'Inter',-apple-system,sans-serif;font-size:0.75rem;"
        f'font-weight:500;">{display_label}</span>'
    )


def render_stat_card(
    title: str,
    value: str,
    subtitle: Optional[str] = None,
    color: str = "#3b82f6"
) -> str:
    """Render a statistics display card."""
    subtitle_html = ""
    if subtitle:
        subtitle_html = (
            f'<div style="color:#64748b;font-family:\'Inter\',-apple-system,sans-serif;'
            f'font-size:0.75rem;margin-top:4px;">{subtitle}</div>'
        )

    return (
        f'<div style="background:#1e293b;border:1px solid #334155;'
        f'border-radius:12px;padding:20px;text-align:center;">'
        f'<div style="color:#94a3b8;font-family:\'Inter\',-apple-system,sans-serif;'
        f'font-size:0.75rem;font-weight:500;text-transform:uppercase;'
        f'letter-spacing:0.05em;margin-bottom:8px;">{title}</div>'
        f'<div style="color:{color};font-family:\'Inter\',-apple-system,sans-serif;'
        f'font-size:1.5rem;font-weight:700;">{value}</div>'
        f'{subtitle_html}</div>'
    )


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

    return (
        f'<div style="background:{bg};border:3px solid {color};border-radius:50%;'
        f'width:160px;height:160px;display:flex;flex-direction:column;'
        f'align-items:center;justify-content:center;margin:0 auto;">'
        f'<div style="font-family:\'Inter\',-apple-system,sans-serif;font-size:2.5rem;'
        f'color:{color};font-weight:700;line-height:1;">{score:.0f}</div>'
        f'<div style="font-family:\'Inter\',-apple-system,sans-serif;font-size:0.875rem;'
        f'color:#94a3b8;margin-top:4px;font-weight:500;">{label}</div></div>'
    )


def render_at_risk_card(
    username: str,
    days_inactive: int,
    total_xp: float,
    role: str
) -> str:
    """Render at-risk member card."""
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

    return (
        f'<div style="background:{urgency_bg};border:1px solid {urgency_color}33;'
        f'border-left:4px solid {urgency_color};border-radius:8px;'
        f'padding:12px 16px;margin:8px 0;">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;">'
        f'<div>'
        f'<div style="color:#f8fafc;font-family:\'Inter\',-apple-system,sans-serif;'
        f'font-size:0.95rem;font-weight:600;">{username}</div>'
        f'<div style="color:#94a3b8;font-family:\'Inter\',-apple-system,sans-serif;'
        f'font-size:0.75rem;margin-top:2px;">'
        f'{role_display_name(role)} | {format_xp(total_xp)} XP</div>'
        f'</div>'
        f'<div style="background:{urgency_color};color:white;padding:6px 12px;'
        f'border-radius:9999px;font-family:\'Inter\',-apple-system,sans-serif;'
        f'font-size:0.75rem;font-weight:600;">{days_inactive} days</div>'
        f'</div></div>'
    )


def render_achievement_card(
    player_name: str,
    achievement_name: str,
    metric: str,
    threshold: int,
    created_at: str
) -> str:
    """Render recent achievement card."""
    return (
        f'<div style="background:rgba(16,185,129,0.1);border:1px solid rgba(16,185,129,0.3);'
        f'border-radius:8px;padding:12px 16px;margin:6px 0;">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;">'
        f'<div>'
        f'<div style="color:#10b981;font-family:\'Inter\',-apple-system,sans-serif;'
        f'font-size:0.875rem;font-weight:600;">{achievement_name}</div>'
        f'<div style="color:#f8fafc;font-family:\'Inter\',-apple-system,sans-serif;'
        f'font-size:0.8rem;margin-top:2px;">{player_name}</div>'
        f'</div>'
        f'<div style="color:#64748b;font-family:\'Inter\',-apple-system,sans-serif;'
        f'font-size:0.7rem;text-align:right;">{created_at}</div>'
        f'</div></div>'
    )


def render_api_status(has_key: bool, member_count: int) -> str:
    """Render API status indicator."""
    if has_key:
        status_color = '#10b981'
        status_text = '100 req/min'
        icon = 'Y'
    else:
        status_color = '#f59e0b'
        status_text = '20 req/min'
        icon = '!'

    return (
        f'<div style="display:flex;align-items:center;gap:8px;padding:8px 12px;'
        f'background:rgba(30,41,59,0.8);border:1px solid #334155;border-radius:8px;'
        f"font-family:'Inter',-apple-system,sans-serif;font-size:0.75rem;\">"
        f'<span style="display:inline-flex;align-items:center;justify-content:center;'
        f'width:18px;height:18px;border-radius:50%;background:{status_color}22;'
        f'color:{status_color};font-weight:600;">{icon}</span>'
        f'<span style="color:#94a3b8;">API Key:</span>'
        f'<span style="color:{status_color};font-weight:500;">{status_text}</span>'
        f'<span style="color:#475569;">|</span>'
        f'<span style="color:#94a3b8;">{member_count} members loaded</span>'
        f'</div>'
    )
