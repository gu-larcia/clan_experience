"""WiseOldMan Clan Analytics Dashboard.

A Streamlit app for tracking OSRS clan activity using the WOM API.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
import requests

import config
from api import WOMClient, parse_datetime
from analysis import (
    analyze_members,
    get_at_risk_members,
    get_retention_rates,
    get_activity_buckets,
)
from charts import (
    activity_donut,
    activity_bars,
    xp_gainers,
    retention_line,
    health_gauge,
    xp_histogram,
)
from styles import CSS


# Page config
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(CSS, unsafe_allow_html=True)


# Cached data loaders
@st.cache_resource
def get_client() -> WOMClient:
    """Singleton API client."""
    api_key = st.secrets.get("WOM_API_KEY") if hasattr(st, "secrets") else None
    return WOMClient(config.WOM_BASE_URL, api_key, config.WOM_USER_AGENT)


@st.cache_data(ttl=config.CACHE_TTL_LONG, show_spinner=False)
def load_group(group_id: int) -> dict | None:
    """Load group details."""
    try:
        return get_client().get_group(group_id)
    except requests.HTTPError as e:
        st.error(f"Failed to load group: {e.response.status_code} {e.response.reason}")
        return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None


@st.cache_data(ttl=config.CACHE_TTL_SHORT, show_spinner=False)
def load_members(group_id: int) -> list:
    """Load members via memberships or hiscores endpoint."""
    try:
        return get_client().get_members(group_id)
    except requests.HTTPError as e:
        st.error(f"Failed to load members: {e.response.status_code} {e.response.reason}")
        if e.response.status_code == 404:
            st.info("Group not found. Check your group ID at wiseoldman.net/groups")
        return []
    except Exception as e:
        st.error(f"Error: {e}")
        return []


@st.cache_data(ttl=config.CACHE_TTL_SHORT, show_spinner=False)
def load_activity(group_id: int, limit: int = 500) -> list:
    """Load group activity feed (joins, leaves, kicks, bans)."""
    try:
        return get_client().get_activity(group_id, limit=limit)
    except Exception:
        return []


@st.cache_data(ttl=config.CACHE_TTL_MEDIUM, show_spinner=False)
def load_gains(group_id: int, metric: str, period: str) -> list:
    """Load XP gains."""
    try:
        return get_client().get_gains(group_id, metric, period)
    except Exception:
        return []


@st.cache_data(ttl=config.CACHE_TTL_LONG, show_spinner=False)
def load_achievements(group_id: int) -> list:
    """Load recent achievements."""
    try:
        return get_client().get_achievements(group_id, limit=30)
    except Exception:
        return []


def fmt_xp(val: float) -> str:
    """Format XP with suffix."""
    if val >= 1_000_000_000:
        return f"{val/1_000_000_000:.2f}B"
    if val >= 1_000_000:
        return f"{val/1_000_000:.1f}M"
    if val >= 1_000:
        return f"{val/1_000:.0f}K"
    return f"{int(val):,}"


def fmt_hours(val: float) -> str:
    """Format hours."""
    if val >= 1000:
        return f"{val/1000:.1f}K hrs"
    return f"{val:.1f} hrs"


def main():
    """Main application."""
    
    # Header
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title(f"{config.APP_ICON} {config.APP_TITLE}")
        st.caption("Tracking clan activity and progression")
    
    # Sidebar
    with st.sidebar:
        st.header("Settings")
        
        group_id = st.number_input(
            "Group ID",
            min_value=1,
            value=config.DEFAULT_GROUP_ID,
            help="Find your group ID at wiseoldman.net/groups",
        )
        
        st.divider()
        
        if st.button("🔄 Refresh", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
        
        st.caption(f"Last refresh: {datetime.now().strftime('%H:%M:%S')}")
    
    # Load data
    with st.spinner("Loading clan data..."):
        group = load_group(group_id)
        raw_members = load_members(group_id)
    
    if not raw_members:
        st.warning("No member data available.")
        st.stop()
    
    # Analyze
    analysis = analyze_members(
        raw_members,
        config.ACTIVITY_THRESHOLDS,
        config.STATUS_COLORS,
    )
    members = analysis["members"]
    
    # Sidebar stats
    with st.sidebar:
        st.divider()
        st.subheader("Quick Stats")
        
        c1, c2 = st.columns(2)
        c1.metric("Total", analysis["total_members"])
        c2.metric("Tracked", analysis.get("tracked_members", analysis["total_members"]))
        
        c1, c2 = st.columns(2)
        c1.metric("Active", analysis["counts"]["active"])
        c2.metric("At Risk", analysis["counts"]["at_risk"])
        
        c1, c2 = st.columns(2)
        c1.metric("Churned", analysis["counts"]["churned"])
        c2.metric("Untracked", analysis["counts"].get("untracked", 0))
        
        if group:
            st.divider()
            st.markdown(f"**{group.get('name', 'Unknown')}**")
            if group.get("description"):
                st.caption(group["description"][:150])
            st.link_button(
                "View on WOM",
                f"https://wiseoldman.net/groups/{group_id}",
                use_container_width=True,
            )
    
    # Tabs
    tabs = st.tabs(["📊 Overview", "👥 Members", "📈 Gains", "⚠️ Churn", "🏆 Achievements", "📋 Activity"])
    
    # Overview tab
    with tabs[0]:
        st.header("Clan Overview")
        
        # Top metrics
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.plotly_chart(health_gauge(analysis["health_score"]), use_container_width=True)
        with c2:
            st.metric("Total XP", fmt_xp(analysis["totals"]["xp"]))
            st.caption(f"Avg: {fmt_xp(analysis['averages']['xp'])}")
        with c3:
            st.metric("Total EHP", fmt_hours(analysis["totals"]["ehp"]))
            st.caption(f"Avg: {fmt_hours(analysis['averages']['ehp'])}")
        with c4:
            st.metric("Total EHB", fmt_hours(analysis["totals"]["ehb"]))
            st.caption(f"Avg: {fmt_hours(analysis['averages']['ehb'])}")
        
        st.divider()
        
        # Charts row 1
        c1, c2 = st.columns(2)
        with c1:
            st.plotly_chart(activity_donut(analysis["counts"]), use_container_width=True)
        with c2:
            buckets = get_activity_buckets(members)
            st.plotly_chart(activity_bars(buckets), use_container_width=True)
        
        # Charts row 2
        c1, c2 = st.columns(2)
        with c1:
            rates = get_retention_rates(members, [7, 14, 30, 60, 90])
            st.plotly_chart(retention_line(rates), use_container_width=True)
        with c2:
            st.plotly_chart(xp_histogram(members), use_container_width=True)
    
    # Members tab
    with tabs[1]:
        st.header("All Members")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            status_filter = st.multiselect(
                "Status",
                ["active", "at_risk", "inactive", "churned", "untracked"],
                default=["active", "at_risk", "inactive", "churned", "untracked"],
            )
        with c2:
            sort_col = st.selectbox("Sort by", ["xp", "days_inactive", "ehp", "ehb", "username"])
        with c3:
            sort_asc = st.checkbox("Ascending", value=False)
        
        filtered = [m for m in members if m["status"] in status_filter]
        filtered.sort(key=lambda x: x.get(sort_col, 0) or 0, reverse=not sort_asc)
        
        df = pd.DataFrame([
            {
                "Username": m["username"],
                "Status": m["status"].replace("_", " ").title(),
                "Days Inactive": m["days_inactive"] if m["days_inactive"] >= 0 else "N/A",
                "Total XP": m["xp"],
                "EHP": round(m["ehp"], 1),
                "EHB": round(m["ehb"], 1),
                "Type": m["type"].title(),
            }
            for m in filtered
        ])
        
        st.dataframe(df, use_container_width=True, hide_index=True)
        st.caption(f"Showing {len(filtered)} of {len(members)} members")
    
    # Gains tab
    with tabs[2]:
        st.header("XP Gains")
        
        c1, c2 = st.columns(2)
        with c1:
            metric = st.selectbox("Skill", config.SKILLS)
        with c2:
            period = st.selectbox("Period", config.PERIODS, index=1)
        
        gains = load_gains(group_id, metric, period)
        
        if gains:
            st.plotly_chart(xp_gainers(gains, metric), use_container_width=True)
            
            # Summary
            total_gained = sum(g.get("data", {}).get("gained", 0) for g in gains)
            active_count = sum(1 for g in gains if g.get("data", {}).get("gained", 0) > 0)
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Total Gained", fmt_xp(total_gained))
            c2.metric("Active Gainers", active_count)
            c3.metric("Avg Gain", fmt_xp(total_gained / max(active_count, 1)))
        else:
            st.info("No gain data for this period.")
    
    # Churn tab
    with tabs[3]:
        st.header("Churn Risk")
        
        c1, c2 = st.columns(2)
        with c1:
            min_days = st.slider("Min days inactive", 7, 60, 14)
        with c2:
            max_days = st.slider("Max days inactive", 30, 180, 90)
        
        at_risk = get_at_risk_members(members, min_days, max_days)
        
        if at_risk:
            # Priority counts
            high = [m for m in at_risk if m["days_inactive"] > 60]
            med = [m for m in at_risk if 30 < m["days_inactive"] <= 60]
            low = [m for m in at_risk if m["days_inactive"] <= 30]
            
            c1, c2, c3 = st.columns(3)
            c1.metric("🔴 High Risk (60+)", len(high))
            c2.metric("🟠 Medium (31-60)", len(med))
            c3.metric("🟡 Low (≤30)", len(low))
            
            st.divider()
            
            for m in at_risk[:25]:
                urgency = "🔴" if m["days_inactive"] > 60 else "🟠" if m["days_inactive"] > 30 else "🟡"
                st.markdown(
                    f"{urgency} **{m['username']}** — {m['days_inactive']} days — "
                    f"{fmt_xp(m['xp'])} XP"
                )
            
            if len(at_risk) > 25:
                st.caption(f"Showing 25 of {len(at_risk)} at-risk members")
        else:
            st.success("No members in the specified risk range.")
    
    # Achievements tab
    with tabs[4]:
        st.header("Recent Achievements")
        
        achievements = load_achievements(group_id)
        
        if achievements:
            for ach in achievements[:20]:
                player = ach.get("player", {})
                name = player.get("displayName", "Unknown")
                title = ach.get("name", "Achievement")
                created = parse_datetime(ach.get("createdAt"))
                time_str = created.strftime("%b %d") if created else "?"
                
                st.markdown(f"🏆 **{title}** — {name} ({time_str})")
        else:
            st.info("No recent achievements.")

    # Activity tab
    with tabs[5]:
        st.header("Group Activity")
        st.caption("Recent joins, leaves, kicks, and role changes")
        
        activity = load_activity(group_id, limit=500)
        
        if activity:
            # Categorize activity
            activity_types = {
                "joined": [],
                "left": [],
                "kicked": [],
                "banned": [],
                "changed_role": [],
                "other": [],
            }
            
            for event in activity:
                event_type = event.get("type", "").lower()
                if event_type in activity_types:
                    activity_types[event_type].append(event)
                else:
                    activity_types["other"].append(event)
            
            # Summary metrics
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Joined", len(activity_types["joined"]))
            c2.metric("Left", len(activity_types["left"]))
            c3.metric("Kicked", len(activity_types["kicked"]))
            c4.metric("Banned", len(activity_types["banned"]))
            
            st.divider()
            
            # Filter options
            c1, c2 = st.columns(2)
            with c1:
                type_filter = st.multiselect(
                    "Event Type",
                    ["joined", "left", "kicked", "banned", "changed_role"],
                    default=["joined", "left", "kicked", "banned"],
                )
            with c2:
                show_limit = st.number_input("Show recent", min_value=10, max_value=500, value=50)
            
            # Filter and display events
            filtered_events = []
            for t in type_filter:
                filtered_events.extend(activity_types.get(t, []))
            
            # Sort by date descending
            filtered_events.sort(
                key=lambda x: x.get("createdAt", ""),
                reverse=True
            )
            
            if filtered_events:
                for event in filtered_events[:show_limit]:
                    player = event.get("player", {})
                    name = player.get("displayName", "Unknown")
                    event_type = event.get("type", "unknown")
                    role = event.get("role", "")
                    prev_role = event.get("previousRole", "")
                    created = parse_datetime(event.get("createdAt"))
                    time_str = created.strftime("%b %d, %Y") if created else "?"
                    
                    # Icon based on event type
                    icons = {
                        "joined": "🟢",
                        "left": "🟡",
                        "kicked": "🔴",
                        "banned": "⛔",
                        "changed_role": "🔄",
                    }
                    icon = icons.get(event_type, "⚪")
                    
                    # Format message
                    if event_type == "changed_role":
                        msg = f"{icon} **{name}** — {prev_role} → {role} ({time_str})"
                    elif event_type == "joined" and role:
                        msg = f"{icon} **{name}** joined as {role} ({time_str})"
                    else:
                        msg = f"{icon} **{name}** {event_type} ({time_str})"
                    
                    st.markdown(msg)
                
                if len(filtered_events) > show_limit:
                    st.caption(f"Showing {show_limit} of {len(filtered_events)} events")
            else:
                st.info("No events match the selected filters.")
            
            # Former members summary
            st.divider()
            st.subheader("Former Members")
            
            former = activity_types["left"] + activity_types["kicked"] + activity_types["banned"]
            if former:
                former_names = set()
                for event in former:
                    player = event.get("player", {})
                    name = player.get("displayName", "Unknown")
                    former_names.add(name)
                
                st.write(f"**{len(former_names)}** unique players have left, been kicked, or banned.")
                
                with st.expander("View former member list"):
                    for name in sorted(former_names):
                        st.text(name)
            else:
                st.info("No former member data in recent activity.")
        else:
            st.info("No activity data available.")


if __name__ == "__main__":
    main()
