"""WiseOldMan Clan Analytics Dashboard v1.0"""

import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timezone

from config import (
    APP_TITLE, APP_ICON, WOM_API_BASE, WOM_GROUP_ID, WOM_USER_AGENT,
    CACHE_TTL_MEMBERS, CACHE_TTL_GAINS, CACHE_TTL_DETAILS,
    ACTIVITY_THRESHOLDS, ACTIVITY_COLORS, GAIN_PERIODS, DEFAULT_GAIN_PERIOD,
    SKILLS,
)
from services import (
    WOMClient, parse_wom_datetime,
    analyze_clan_activity, get_churn_risk_members,
    calculate_retention_rates, group_by_role, get_activity_timeline,
)
from ui import (
    OSRS_CSS,
    render_status_badge, render_stat_card, render_health_score_display,
    render_at_risk_card, render_achievement_card,
    create_activity_donut, create_activity_timeline, create_xp_gains_chart,
    create_role_distribution, create_retention_chart, create_xp_distribution,
    create_ehp_vs_ehb_scatter, create_health_gauge,
)
from utils import (
    format_xp, format_number, format_hours, format_percentage,
    format_time_ago, format_date, role_display_name,
)

# Page config
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom CSS
st.markdown(OSRS_CSS, unsafe_allow_html=True)


# ===== Cached Data Fetching =====

@st.cache_resource
def get_api_client() -> WOMClient:
    """Get singleton API client."""
    # Check for API key in secrets
    api_key = st.secrets.get("WOM_API_KEY", None) if hasattr(st, 'secrets') else None
    return WOMClient(
        base_url=WOM_API_BASE,
        api_key=api_key,
        user_agent=WOM_USER_AGENT
    )


@st.cache_data(ttl=CACHE_TTL_DETAILS, show_spinner=False)
def fetch_group_details(_client: WOMClient, group_id: int) -> dict:
    """Fetch group details."""
    try:
        return _client.get_group_details(group_id)
    except requests.exceptions.HTTPError as e:
        st.error(f"Group API Error: {e.response.status_code} - {e.response.reason}")
        st.caption(f"URL: {e.response.url}")
        return {}
    except Exception as e:
        st.error(f"Failed to fetch group details: {type(e).__name__}: {e}")
        return {}


@st.cache_data(ttl=CACHE_TTL_MEMBERS, show_spinner=False)
def fetch_members(_client: WOMClient, group_id: int) -> list:
    """Fetch group members via hiscores endpoint."""
    try:
        return _client.get_group_members(group_id)
    except requests.exceptions.HTTPError as e:
        st.error(f"API Error: {e.response.status_code} - {e.response.reason}")
        st.caption(f"URL: {e.response.url}")
        return []
    except Exception as e:
        st.error(f"Failed to fetch members: {type(e).__name__}: {e}")
        return []


@st.cache_data(ttl=CACHE_TTL_GAINS, show_spinner=False)
def fetch_gains(_client: WOMClient, group_id: int, metric: str, period: str) -> list:
    """Fetch XP gains."""
    try:
        return _client.get_group_gains(group_id, metric=metric, period=period)
    except Exception as e:
        st.error(f"Failed to fetch gains: {e}")
        return []


@st.cache_data(ttl=CACHE_TTL_DETAILS, show_spinner=False)
def fetch_achievements(_client: WOMClient, group_id: int, limit: int = 25) -> list:
    """Fetch recent achievements."""
    try:
        return _client.get_group_achievements(group_id, limit=limit)
    except Exception as e:
        return []


@st.cache_data(ttl=CACHE_TTL_DETAILS, show_spinner=False)
def fetch_competitions(_client: WOMClient, group_id: int) -> list:
    """Fetch competitions."""
    try:
        return _client.get_group_competitions(group_id)
    except Exception as e:
        return []


def main():
    """Main application."""
    
    # Header
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title(f"{APP_ICON} {APP_TITLE}")
        st.caption("*Tracking clan activity and progression*")
    with col2:
        st.link_button(
            "View on WOM",
            f"https://wiseoldman.net/groups/{WOM_GROUP_ID}",
            use_container_width=True
        )
    
    # Initialize client and fetch data
    client = get_api_client()
    
    with st.spinner("Loading clan data..."):
        group_details = fetch_group_details(client, WOM_GROUP_ID)
        members_raw = fetch_members(client, WOM_GROUP_ID)
    
    if not members_raw:
        st.error("Unable to load clan data. Please check your connection and try again.")
        return
    
    # Analyze activity
    analysis = analyze_clan_activity(members_raw, ACTIVITY_THRESHOLDS, ACTIVITY_COLORS)
    
    # Sidebar
    with st.sidebar:
        st.header("Clan Info")
        
        if group_details:
            st.markdown(f"### {group_details.get('name', 'Unknown Clan')}")
            if group_details.get('description'):
                st.caption(group_details['description'][:200])
            
            st.divider()
        
        # Quick stats
        st.subheader("Quick Stats")
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Members", analysis['total_members'])
        with col2:
            st.metric("Active", analysis['status_counts']['active'])
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("At Risk", analysis['status_counts']['at_risk'])
        with col2:
            st.metric("Churned", analysis['status_counts']['churned'])
        
        st.divider()
        
        # Activity thresholds config
        st.subheader("Settings")
        
        with st.expander("Activity Thresholds"):
            st.caption("Days to classify as:")
            active_days = st.number_input("Active", value=ACTIVITY_THRESHOLDS['active'], min_value=1, max_value=30)
            at_risk_days = st.number_input("At Risk", value=ACTIVITY_THRESHOLDS['at_risk'], min_value=7, max_value=90)
            inactive_days = st.number_input("Inactive", value=ACTIVITY_THRESHOLDS['inactive'], min_value=30, max_value=180)
        
        st.divider()
        
        # Refresh button
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.toast("Data refreshed!")
            st.rerun()
        
        st.caption(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")
    
    # Main content tabs
    tabs = st.tabs([
        "📊 Overview",
        "👥 Members",
        "📈 XP Gains",
        "⚠️ Churn Risk",
        "🏆 Achievements",
    ])
    
    # ===== Tab 1: Overview =====
    with tabs[0]:
        st.header("Clan Overview")
        
        # Top row: Health score and key metrics
        col1, col2, col3, col4 = st.columns([1.5, 1, 1, 1])
        
        with col1:
            st.markdown(render_health_score_display(analysis['health_score']), unsafe_allow_html=True)
        
        with col2:
            st.markdown(render_stat_card(
                "Total XP",
                format_xp(analysis['total_xp']),
                f"Avg: {format_xp(analysis['avg_xp'])}"
            ), unsafe_allow_html=True)
        
        with col3:
            st.markdown(render_stat_card(
                "Total EHP",
                format_hours(analysis['total_ehp']),
                f"Avg: {format_hours(analysis['avg_ehp'])}"
            ), unsafe_allow_html=True)
        
        with col4:
            st.markdown(render_stat_card(
                "Total EHB",
                format_hours(analysis['total_ehb']),
                f"Avg: {format_hours(analysis['avg_ehb'])}"
            ), unsafe_allow_html=True)
        
        st.divider()
        
        # Activity charts row
        col1, col2 = st.columns(2)
        
        with col1:
            fig = create_activity_donut(analysis['status_counts'])
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            timeline = get_activity_timeline(analysis['members'])
            fig = create_activity_timeline(timeline)
            st.plotly_chart(fig, use_container_width=True)
        
        # Retention and role distribution
        col1, col2 = st.columns(2)
        
        with col1:
            retention = calculate_retention_rates(analysis['members'], [7, 14, 30, 60, 90])
            fig = create_retention_chart(retention)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            role_groups = group_by_role(analysis['members'])
            role_counts = {role: len(members) for role, members in role_groups.items()}
            fig = create_role_distribution(role_counts)
            st.plotly_chart(fig, use_container_width=True)
    
    # ===== Tab 2: Members =====
    with tabs[1]:
        st.header("All Members")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            status_filter = st.multiselect(
                "Filter by Status",
                options=['active', 'at_risk', 'inactive', 'churned'],
                default=['active', 'at_risk', 'inactive', 'churned'],
                format_func=lambda x: x.replace('_', ' ').title()
            )
        with col2:
            role_filter = st.multiselect(
                "Filter by Role",
                options=list(set(m['role'] for m in analysis['members'])),
                format_func=role_display_name
            )
        with col3:
            sort_by = st.selectbox(
                "Sort by",
                options=['Total XP', 'Last Active', 'EHP', 'EHB', 'Username'],
            )
        
        # Filter and sort members
        filtered_members = analysis['members']
        
        if status_filter:
            filtered_members = [m for m in filtered_members if m['activity_status'] in status_filter]
        
        if role_filter:
            filtered_members = [m for m in filtered_members if m['role'] in role_filter]
        
        # Sort
        sort_map = {
            'Total XP': ('exp', True),
            'Last Active': ('days_inactive', False),
            'EHP': ('ehp', True),
            'EHB': ('ehb', True),
            'Username': ('username', False),
        }
        sort_key, reverse = sort_map.get(sort_by, ('exp', True))
        
        if sort_key == 'username':
            filtered_members = sorted(filtered_members, key=lambda x: x.get(sort_key, '').lower(), reverse=reverse)
        else:
            filtered_members = sorted(filtered_members, key=lambda x: x.get(sort_key, 0) or 0, reverse=reverse)
        
        # Display as dataframe
        if filtered_members:
            df_data = []
            for m in filtered_members:
                df_data.append({
                    'Username': m['username'],
                    'Role': role_display_name(m['role']),
                    'Status': m['activity_status'].replace('_', ' ').title(),
                    'Days Inactive': m['days_inactive'] if m['days_inactive'] >= 0 else 'N/A',
                    'Total XP': m['exp'],
                    'EHP': round(m['ehp'], 1) if m['ehp'] else 0,
                    'EHB': round(m['ehb'], 1) if m['ehb'] else 0,
                    'Type': m['type'].title(),
                })
            
            df = pd.DataFrame(df_data)
            
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
                column_config={
                    'Username': st.column_config.TextColumn('Username', width='medium'),
                    'Role': st.column_config.TextColumn('Role'),
                    'Status': st.column_config.TextColumn('Status'),
                    'Days Inactive': st.column_config.NumberColumn('Days Inactive'),
                    'Total XP': st.column_config.NumberColumn('Total XP', format='%d'),
                    'EHP': st.column_config.NumberColumn('EHP', format='%.1f'),
                    'EHB': st.column_config.NumberColumn('EHB', format='%.1f'),
                    'Type': st.column_config.TextColumn('Type'),
                }
            )
            
            st.caption(f"Showing {len(filtered_members)} of {len(analysis['members'])} members")
        
        # XP Distribution chart
        st.subheader("XP Distribution")
        col1, col2 = st.columns(2)
        with col1:
            fig = create_xp_distribution(filtered_members)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = create_ehp_vs_ehb_scatter(filtered_members)
            st.plotly_chart(fig, use_container_width=True)
    
    # ===== Tab 3: XP Gains =====
    with tabs[2]:
        st.header("XP Gains")
        
        col1, col2 = st.columns(2)
        with col1:
            metric = st.selectbox(
                "Skill/Metric",
                options=SKILLS,
                format_func=lambda x: x.title()
            )
        with col2:
            period = st.selectbox(
                "Time Period",
                options=GAIN_PERIODS,
                index=GAIN_PERIODS.index(DEFAULT_GAIN_PERIOD),
                format_func=lambda x: x.title()
            )
        
        with st.spinner(f"Loading {metric} gains..."):
            gains = fetch_gains(client, WOM_GROUP_ID, metric, period)
        
        if gains:
            # Top gainers chart
            fig = create_xp_gains_chart(gains, metric)
            st.plotly_chart(fig, use_container_width=True)
            
            # Gains table
            st.subheader("All Gains")
            
            gains_data = []
            for g in gains:
                player = g.get('player', {})
                data = g.get('data', {})
                gained = data.get('gained', 0)
                if gained > 0:
                    gains_data.append({
                        'Username': player.get('displayName', 'Unknown'),
                        'Gained': gained,
                        'Start': data.get('start', 0),
                        'End': data.get('end', 0),
                    })
            
            if gains_data:
                gains_df = pd.DataFrame(gains_data)
                gains_df = gains_df.sort_values('Gained', ascending=False)
                
                st.dataframe(
                    gains_df,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        'Username': st.column_config.TextColumn('Username', width='medium'),
                        'Gained': st.column_config.NumberColumn('XP Gained', format='%d'),
                        'Start': st.column_config.NumberColumn('Start XP', format='%d'),
                        'End': st.column_config.NumberColumn('End XP', format='%d'),
                    }
                )
                
                # Summary stats
                total_gained = sum(g['Gained'] for g in gains_data)
                avg_gained = total_gained / len(gains_data) if gains_data else 0
                active_gainers = len([g for g in gains_data if g['Gained'] > 0])
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Gained", format_xp(total_gained))
                with col2:
                    st.metric("Average Gain", format_xp(avg_gained))
                with col3:
                    st.metric("Active Gainers", f"{active_gainers}/{len(gains)}")
        else:
            st.info("No gain data available for this period.")
    
    # ===== Tab 4: Churn Risk =====
    with tabs[3]:
        st.header("Churn Risk Analysis")
        
        st.markdown("""
        Members shown here haven't been active recently and may be at risk of leaving the clan.
        Consider reaching out to re-engage them.
        """)
        
        col1, col2 = st.columns(2)
        with col1:
            min_days = st.slider("Minimum days inactive", 7, 60, 14)
        with col2:
            max_days = st.slider("Maximum days inactive", 30, 180, 90)
        
        at_risk = get_churn_risk_members(analysis['members'], min_days, max_days)
        
        if at_risk:
            st.subheader(f"⚠️ {len(at_risk)} Members at Risk")
            
            # Priority breakdown
            high_risk = [m for m in at_risk if m['days_inactive'] > 45]
            medium_risk = [m for m in at_risk if 30 < m['days_inactive'] <= 45]
            low_risk = [m for m in at_risk if m['days_inactive'] <= 30]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("🔴 High Risk (45+ days)", len(high_risk))
            with col2:
                st.metric("🟠 Medium Risk (31-45 days)", len(medium_risk))
            with col3:
                st.metric("🟡 Low Risk (14-30 days)", len(low_risk))
            
            st.divider()
            
            # Display at-risk members
            for member in at_risk[:20]:  # Limit display
                st.markdown(
                    render_at_risk_card(
                        username=member['username'],
                        days_inactive=member['days_inactive'],
                        total_xp=member['exp'],
                        role=member['role']
                    ),
                    unsafe_allow_html=True
                )
            
            if len(at_risk) > 20:
                st.caption(f"Showing 20 of {len(at_risk)} at-risk members")
        else:
            st.success("🎉 No members currently at significant churn risk!")
    
    # ===== Tab 5: Achievements =====
    with tabs[4]:
        st.header("Recent Achievements")
        
        achievements = fetch_achievements(client, WOM_GROUP_ID, limit=50)
        
        if achievements:
            for ach in achievements[:25]:
                player = ach.get('player', {})
                created = parse_wom_datetime(ach.get('createdAt'))
                
                st.markdown(
                    render_achievement_card(
                        player_name=player.get('displayName', 'Unknown'),
                        achievement_name=ach.get('name', 'Achievement'),
                        metric=ach.get('metric', ''),
                        threshold=ach.get('threshold', 0),
                        created_at=format_time_ago(created)
                    ),
                    unsafe_allow_html=True
                )
        else:
            st.info("No recent achievements to display.")
        
        # Competitions section
        st.divider()
        st.subheader("Competitions")
        
        competitions = fetch_competitions(client, WOM_GROUP_ID)
        
        if competitions:
            active_comps = [c for c in competitions if c.get('endsAt') and parse_wom_datetime(c['endsAt']) and parse_wom_datetime(c['endsAt']) > datetime.now(timezone.utc)]
            past_comps = [c for c in competitions if c not in active_comps][:5]
            
            if active_comps:
                st.markdown("#### 🏃 Active Competitions")
                for comp in active_comps:
                    ends_at = parse_wom_datetime(comp.get('endsAt'))
                    st.markdown(f"""
                    **{comp.get('title', 'Competition')}**  
                    Metric: {comp.get('metric', 'unknown').title()} | Ends: {format_date(ends_at, include_time=True)}
                    """)
            
            if past_comps:
                st.markdown("#### 📜 Recent Competitions")
                for comp in past_comps:
                    ended_at = parse_wom_datetime(comp.get('endsAt'))
                    st.markdown(f"""
                    **{comp.get('title', 'Competition')}**  
                    Metric: {comp.get('metric', 'unknown').title()} | Ended: {format_time_ago(ended_at)}
                    """)
        else:
            st.info("No competitions found.")


if __name__ == "__main__":
    main()
