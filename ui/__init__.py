"""UI components, charts, and styles."""

from .styles import MODERN_CSS
from .components import (
    render_status_badge,
    render_stat_card,
    render_health_score_display,
    render_at_risk_card,
    render_achievement_card,
    render_api_status,
)
from .charts import (
    create_activity_donut,
    create_activity_timeline,
    create_xp_gains_chart,
    create_role_distribution,
    create_retention_chart,
    create_xp_distribution,
    create_ehp_vs_ehb_scatter,
    create_health_gauge,
    CHART_COLORS,
)

__all__ = [
    'MODERN_CSS',
    'render_status_badge',
    'render_stat_card',
    'render_health_score_display',
    'render_at_risk_card',
    'render_achievement_card',
    'render_api_status',
    'create_activity_donut',
    'create_activity_timeline',
    'create_xp_gains_chart',
    'create_role_distribution',
    'create_retention_chart',
    'create_xp_distribution',
    'create_ehp_vs_ehb_scatter',
    'create_health_gauge',
    'CHART_COLORS',
]
