import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# PAGE CONFIGURATION
st.set_page_config(
    page_title="Nimbus BI Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CREATE SAMPLE DATA
@st.cache_data
def load_data():
    np.random.seed(42)

    regions = ["APAC", "EMEA", "North America", "LATAM"]
    plans = ["Enterprise", "Pro", "Starter"]

    owners = [
        "Hannah Kim", "Mel Tanaka", "Ethan Brooks",
        "Liam Walsh", "Diego Alvarez", "Noor Haddad"
    ]

    industries = [
        "Fintech", "Healthcare", "Retail",
        "Manufacturing", "Media", "Logistics"
    ]

    account_names = [
        "Fjordline Bio", "Umbra Labs", "Tidewater Foods",
        "Basalt Foods", "Evergreen Logistics", "Keystone Analytics",
        "Tidewater Health", "Driftwood Foods", "Evergreen Labs",
        "Ionix Foods", "Ionix Analytics", "Quartzite Capital",
        "Vantage Foods", "Zephyr Robotics", "Keystone Energy",
        "Meridian Media", "Foxglove Systems", "Willowmore Media",
        "Apex Logistics", "Solstice Logistics", "Lumora Bio",
        "Delta Nine Health", "Orchid Labs", "Juniper Media"
    ]

    # ACCOUNT DATA
    account_data = []

    for i in range(220):
        name = account_names[i % len(account_names)]
        plan = np.random.choice(plans, p=[0.45, 0.35, 0.20])
        mrr = np.random.randint(600, 80000)
        health = np.random.randint(35, 101)

        if health >= 80:
            status = "Healthy"
        elif health >= 60:
            status = "Needs attention"
        else:
            status = "At risk"

        account_data.append({
            "Account": name if i < len(account_names) else f"{name} {i}",
            "Plan": plan,
            "MRR": mrr,
            "Health": health,
            "Status": status,
            "Region": np.random.choice(regions),
            "Industry": np.random.choice(industries),
            "Owner": np.random.choice(owners),
            "Renewal": (
                datetime.today().date()
                + timedelta(days=int(np.random.randint(1, 500)))
            ),
            "Products": ", ".join(np.random.choice(
                ["Analytics", "Automation", "AI copilot", "Data sync", "Security"],
                size=3,
                replace=False
            )),
            "Trend": np.random.randint(1000, 80000)
        })

    accounts = pd.DataFrame(account_data)

    # DEAL DATA
    stages = [
        "Prospecting", "Discovery", "Proposal",
        "Negotiation", "Closed won", "Closed lost"
    ]

    probabilities = {
        "Prospecting": 10,
        "Discovery": 25,
        "Proposal": 50,
        "Negotiation": 75,
        "Closed won": 100,
        "Closed lost": 0
    }

    deal_data = []

    for i in range(200):
        stage = np.random.choice(
            stages,
            p=[0.30, 0.25, 0.20, 0.12, 0.08, 0.05]
        )

        amount = np.random.randint(3000, 200000)

        deal_data.append({
            "Account": np.random.choice(account_names),
            "Stage": stage,
            "Amount": amount,
            "Probability": probabilities[stage],
            "Weighted": amount * probabilities[stage] / 100,
            "Expected close": (
                datetime.today()
                + timedelta(days=int(np.random.randint(1, 90)))
            ).date(),
            "Owner": np.random.choice(owners),
            "Source": np.random.choice(
                ["Inbound", "Outbound", "Partner", "Events"]
            ),
            "Plan": np.random.choice(plans),
            "Region": np.random.choice(regions)
        })

    deals = pd.DataFrame(deal_data)

    # REVENUE DATA
    months = pd.date_range(
        end=datetime.today(),
        periods=24,
        freq="ME"
    )

    revenue = pd.DataFrame({
        "Month": months,
        "Enterprise": (
            np.linspace(400000, 1000000, 24)
            + np.random.randint(-30000, 30000, 24)
        ),
        "Pro": (
            np.linspace(250000, 600000, 24)
            + np.random.randint(-20000, 20000, 24)
        ),
        "Starter": (
            np.linspace(100000, 250000, 24)
            + np.random.randint(-10000, 10000, 24)
        )
    })

    revenue["Total"] = (
        revenue["Enterprise"]
        + revenue["Pro"]
        + revenue["Starter"]
    )

    return accounts, deals, revenue, regions, plans, stages


accounts, deals, revenue_data, regions, plans, stages = load_data()

# HELPER FUNCTIONS
def money(value):
    if value >= 1000000:
        return f"${value / 1000000:.2f}M"
    if value >= 1000:
        return f"${value / 1000:.1f}K"
    return f"${value:,.0f}"


def page_heading(title, subtitle=None):
    st.subheader(title)
    if subtitle:
        st.caption(subtitle)


# SIDEBAR
st.sidebar.title("📊 Nimbus BI")
st.sidebar.divider()

page = st.sidebar.radio(
    "Navigation",
    ["Overview", "Accounts", "Pipeline"]
)

st.sidebar.divider()
st.sidebar.subheader("Dashboard Filters")

period = st.sidebar.selectbox(
    "Time Period",
    ["3M", "6M", "12M", "24M"],
    index=3
)

region_filter = st.sidebar.multiselect(
    "Region",
    regions,
    default=regions
)

plan_filter = st.sidebar.multiselect(
    "Plan",
    plans,
    default=plans
)

period_months = {
    "3M": 3,
    "6M": 6,
    "12M": 12,
    "24M": 24
}

selected_months = period_months[period]

# APPLY FILTERS
filtered_accounts = accounts[
    accounts["Region"].isin(region_filter)
    & accounts["Plan"].isin(plan_filter)
].copy()

filtered_deals = deals[
    deals["Region"].isin(region_filter)
    & deals["Plan"].isin(plan_filter)
].copy()

filtered_revenue = revenue_data.tail(selected_months).copy()

# HEADER
header_left, header_right = st.columns([4, 1])

with header_left:
    st.title("📊 Nimbus BI")
    st.caption("Business Intelligence Dashboard | Accounts, revenue and sales")

with header_right:
    st.write("")
    st.download_button(
        "📥 Export Accounts",
        data=filtered_accounts.to_csv(index=False).encode("utf-8"),
        file_name="accounts.csv",
        mime="text/csv",
        use_container_width=True
    )

st.divider()

# ==========================================
# OVERVIEW DASHBOARD
# ==========================================
if page == "Overview":

    page_heading(
        "Overview",
        f"All selected regions and plans | Last {selected_months} months"
    )

    page_heading("Revenue")

    total_revenue = filtered_revenue["Total"].sum()
    current_mrr = filtered_revenue["Total"].iloc[-1]

    previous_mrr = (
        filtered_revenue["Total"].iloc[-2]
        if len(filtered_revenue) > 1
        else current_mrr
    )

    growth = (
        (current_mrr - previous_mrr) / previous_mrr * 100
        if previous_mrr != 0 else 0
    )

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Annual recurring revenue",
        money(current_mrr * 12),
        f"{growth:.1f}%"
    )

    c2.metric(
        "Net new MRR",
        money(current_mrr - previous_mrr),
        f"{growth:.1f}%"
    )

    c3.metric(
        "Net revenue retention",
        "126.6%",
        "+4.5 pts"
    )

    c4.metric(
        "Monthly gross churn",
        "1.1%",
        "-0.1 pts"
    )

    st.divider()

    # MRR BY PLAN
    page_heading(
        "MRR by plan",
        "Monthly recurring revenue stacked by subscription plan"
    )

    revenue_fig = go.Figure()

    for column, color in [
        ("Enterprise", "#5B57D2"),
        ("Pro", "#1EA08C"),
        ("Starter", "#F0783C")
    ]:
        revenue_fig.add_trace(go.Scatter(
            x=filtered_revenue["Month"],
            y=filtered_revenue[column],
            name=column,
            stackgroup="one",
            line=dict(color=color)
        ))

    revenue_fig.update_layout(
        height=360,
        template="plotly_white",
        hovermode="x unified",
        yaxis_title="Revenue ($)"
    )

    st.plotly_chart(revenue_fig, use_container_width=True)

    # MRR BRIDGE
    page_heading(
        "MRR bridge",
        "Illustrative movement in monthly recurring revenue"
    )

    bridge_fig = go.Figure(go.Waterfall(
        orientation="v",
        measure=["absolute", "relative", "relative", "relative", "total"],
        x=["Start", "New", "Expansion", "Churn", "End"],
        y=[740000, 642000, 544000, -118000, 0],
        text=["$740K", "+$642K", "+$544K", "-$118K", ""],
        connector={"line": {"color": "gray"}},
        increasing={"marker": {"color": "#159D8B"}},
        decreasing={"marker": {"color": "#E87943"}},
        totals={"marker": {"color": "#5B57D2"}}
    ))

    bridge_fig.update_layout(
        height=350,
        template="plotly_white",
        showlegend=False
    )

    st.plotly_chart(bridge_fig, use_container_width=True)

    # CUSTOMER ACTIVITY HEATMAP
    page_heading(
        "When customers use Nimbus",
        "Illustrative product sessions by weekday and hour"
    )

    heatmap_data = np.random.randint(10, 100, size=(7, 24))

    heatmap_fig = px.imshow(
        heatmap_data,
        x=[f"{hour:02d}:00" for hour in range(24)],
        y=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
        color_continuous_scale="Purples",
        aspect="auto",
        labels={"x": "Hour", "y": "Day", "color": "Sessions"}
    )

    heatmap_fig.update_layout(
        height=320,
        template="plotly_white"
    )

    st.plotly_chart(heatmap_fig, use_container_width=True)

    # REVENUE BY INDUSTRY
    page_heading(
        "Revenue by industry",
        "Revenue distribution across customer industries"
    )

    industry_data = (
        filtered_accounts.groupby("Industry", as_index=False)["MRR"]
        .sum()
        .sort_values("MRR", ascending=False)
    )

    left, right = st.columns(2)

    with left:
        if not industry_data.empty:
            donut_fig = px.pie(
                industry_data,
                names="Industry",
                values="MRR",
                hole=0.60,
                color_discrete_sequence=px.colors.qualitative.Bold
            )

            donut_fig.update_layout(
                height=360,
                template="plotly_white",
                annotations=[{
                    "text": money(industry_data["MRR"].sum()),
                    "x": 0.5,
                    "y": 0.5,
                    "font_size": 20,
                    "showarrow": False
                }]
            )

            st.plotly_chart(donut_fig, use_container_width=True)
        else:
            st.info("No account data matches the selected filters.")

    with right:
        st.markdown("#### Industry revenue details")

        st.dataframe(
            industry_data,
            hide_index=True,
            use_container_width=True
        )

    # TOP ACCOUNTS
    page_heading(
        "Top accounts",
        "Largest customers by monthly recurring revenue"
    )

    top_accounts = filtered_accounts.nlargest(10, "MRR")

    st.dataframe(
        top_accounts[
            ["Account", "Plan", "MRR", "Health", "Renewal"]
        ],
        hide_index=True,
        use_container_width=True
    )


# ==========================================
# ACCOUNTS DASHBOARD
# ==========================================
elif page == "Accounts":

    page_heading(
        "Accounts",
        "Explore customers, account health and upcoming renewals"
    )

    page_heading("Customer book")

    search = st.text_input(
        "🔍 Search by account, owner or industry"
    )

    if search:
        search_mask = (
            filtered_accounts["Account"].str.contains(
                search, case=False, na=False
            )
            | filtered_accounts["Owner"].str.contains(
                search, case=False, na=False
            )
            | filtered_accounts["Industry"].str.contains(
                search, case=False, na=False
            )
        )

        filtered_accounts = filtered_accounts[search_mask]

    status_filter = st.multiselect(
        "Customer health",
        ["Healthy", "Needs attention", "At risk"],
        default=["Healthy", "Needs attention", "At risk"]
    )

    filtered_accounts = filtered_accounts[
        filtered_accounts["Status"].isin(status_filter)
    ]

    # HEALTH VS REVENUE
    page_heading(
        "Health vs. revenue",
        "Each bubble represents an account; bubble size represents MRR"
    )

    if not filtered_accounts.empty:
        scatter_fig = px.scatter(
            filtered_accounts,
            x="Health",
            y="MRR",
            size="MRR",
            color="Plan",
            hover_name="Account",
            hover_data=["Owner", "Status", "Industry"],
            log_y=True,
            color_discrete_map={
                "Enterprise": "#655CD6",
                "Pro": "#23A896",
                "Starter": "#E87943"
            }
        )

        scatter_fig.update_layout(
            height=450,
            template="plotly_white",
            xaxis_title="Health score",
            yaxis_title="MRR ($)"
        )

        st.plotly_chart(scatter_fig, use_container_width=True)
    else:
        st.info("No accounts match the selected filters.")

    # UPCOMING RENEWALS
    page_heading(
        "Upcoming renewals",
        "Renewals due in the next 90 days"
    )

    today = datetime.today().date()

    renewals = filtered_accounts[
        (filtered_accounts["Renewal"] >= today)
        & (filtered_accounts["Renewal"] <= today + timedelta(days=90))
    ].sort_values("Renewal")

    st.caption(f"{len(renewals)} accounts")

    st.dataframe(
        renewals[
            ["Account", "Renewal", "MRR", "Plan", "Status"]
        ].head(15),
        hide_index=True,
        use_container_width=True
    )

    # ALL ACCOUNTS
    page_heading(
        "All accounts",
        "Sorted by MRR, largest first"
    )

    all_accounts = filtered_accounts.sort_values(
        "MRR",
        ascending=False
    )

    st.caption(f"{len(all_accounts)} accounts")

    st.dataframe(
        all_accounts[
            [
                "Account", "Plan", "MRR", "Trend", "Health",
                "Status", "Products", "Owner", "Region"
            ]
        ],
        hide_index=True,
        use_container_width=True,
        height=450
    )

    st.download_button(
        "📥 Download All Accounts",
        data=all_accounts.to_csv(index=False).encode("utf-8"),
        file_name="all_accounts.csv",
        mime="text/csv"
    )


# ==========================================
# PIPELINE DASHBOARD
# ==========================================
elif page == "Pipeline":

    page_heading(
        "Pipeline",
        "Explore sales opportunities, forecasts and deal progress"
    )

    page_heading("Pipeline health")

    open_deals = filtered_deals[
        ~filtered_deals["Stage"].isin(
            ["Closed won", "Closed lost"]
        )
    ]

    closed_deals = filtered_deals[
        filtered_deals["Stage"].isin(
            ["Closed won", "Closed lost"]
        )
    ]

    won_deals = filtered_deals[
        filtered_deals["Stage"] == "Closed won"
    ]

    open_pipeline = open_deals["Amount"].sum()
    weighted_forecast = open_deals["Weighted"].sum()

    win_rate = (
        len(won_deals) / len(closed_deals) * 100
        if len(closed_deals) > 0 else 0
    )

    avg_sales_cycle = 43

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Open pipeline",
        money(open_pipeline),
        f"{len(open_deals)} deals"
    )

    c2.metric(
        "Weighted forecast",
        money(weighted_forecast),
        "Open deals"
    )

    c3.metric(
        "Win rate",
        f"{win_rate:.0f}%",
        f"{len(won_deals)} won deals"
    )

    c4.metric(
        "Avg. sales cycle",
        f"{avg_sales_cycle} days",
        "Illustrative value"
    )

    st.divider()

    # BOOKINGS BY MONTH
    page_heading(
        "Bookings by month",
        "Illustrative closed-won value and projected bookings"
    )

    booking_fig = go.Figure()

    booking_fig.add_trace(go.Bar(
        x=["Sep 26", "Oct 26", "Nov 26"],
        y=[0, 270000, 125000],
        name="Closed won",
        marker_color="#5B57D2"
    ))

    booking_fig.add_trace(go.Bar(
        x=["Sep 26", "Oct 26", "Nov 26"],
        y=[0, 0, 55000],
        name="Projected",
        marker_color="#27A991"
    ))

    booking_fig.update_layout(
        barmode="stack",
        height=350,
        template="plotly_white",
        yaxis_title="Bookings ($)"
    )

    st.plotly_chart(booking_fig, use_container_width=True)

    # QUARTER BOOKINGS
    page_heading(
        "Quarter bookings",
        "Closed-won value against the quarter target"
    )

    quarter_target = 457000
    quarter_achieved = 398000
    achievement = quarter_achieved / quarter_target * 100

    gauge_fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=achievement,
        number={"suffix": "%", "font": {"size": 35}},
        title={
            "text": f"{money(quarter_achieved)} of {money(quarter_target)}"
        },
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "#5B57D2"},
            "bgcolor": "#EEEEF5",
            "steps": [
                {"range": [0, 100], "color": "#EEEEF5"}
            ]
        }
    ))

    gauge_fig.update_layout(
        height=350,
        template="plotly_white"
    )

    st.plotly_chart(gauge_fig, use_container_width=True)

    # PIPELINE FLOW
    page_heading(
        "Pipeline flow",
        "Illustrative deal flow from source to plan and outcome"
    )

    sankey_fig = go.Figure(go.Sankey(
        node={
            "pad": 20,
            "thickness": 18,
            "line": {"color": "white", "width": 1},
            "label": [
                "Inbound", "Outbound", "Partner", "Events",
                "Enterprise", "Pro", "Starter", "Won", "Open", "Lost"
            ],
            "color": [
                "#7772DD", "#B2B0F0", "#C7C5F3", "#D5D3F7",
                "#5550C8", "#8884DC", "#B9B6EE",
                "#28A991", "#5550C8", "#E87943"
            ]
        },
        link={
            "source": [
                0, 0, 0, 1, 1, 2, 2,
                3, 3, 4, 4, 5, 5, 6
            ],
            "target": [
                4, 5, 8, 4, 5, 4, 6,
                4, 6, 7, 8, 7, 8, 9
            ],
            "value": [
                20, 10, 10, 15, 10, 12, 8,
                10, 8, 15, 30, 10, 20, 8
            ],
            "color": ["rgba(100,90,210,0.25)"] * 14
        }
    ))

    sankey_fig.update_layout(
        height=370,
        template="plotly_white"
    )

    st.plotly_chart(sankey_fig, use_container_width=True)

    # STAGE CONVERSION
    page_heading(
        "Stage conversion",
        "Number of deals in each sales stage"
    )

    stage_counts = (
        filtered_deals.groupby("Stage")
        .size()
        .reindex(stages, fill_value=0)
        .rename("Deals")
        .reset_index()
    )

    stage_conversion = stage_counts[
        stage_counts["Stage"].isin([
            "Prospecting", "Discovery", "Proposal",
            "Negotiation", "Closed won"
        ])
    ]

    funnel_fig = px.funnel(
        stage_conversion,
        x="Deals",
        y="Stage",
        color_discrete_sequence=["#5B57D2"]
    )

    funnel_fig.update_layout(
        height=400,
        template="plotly_white"
    )

    st.plotly_chart(funnel_fig, use_container_width=True)

    # OPEN PIPELINE BY OWNER
    page_heading(
        "Open pipeline by owner",
        "Total open deal value assigned to each sales owner"
    )

    owner_data = (
        open_deals.groupby("Owner", as_index=False)["Amount"]
        .sum()
        .sort_values("Amount", ascending=True)
    )

    owner_fig = px.bar(
        owner_data,
        x="Amount",
        y="Owner",
        orientation="h",
        text="Amount",
        color_discrete_sequence=["#5B57D2"]
    )

    owner_fig.update_traces(
        texttemplate="$%{x:,.0f}",
        textposition="outside"
    )

    owner_fig.update_layout(
        height=400,
        template="plotly_white",
        showlegend=False
    )

    st.plotly_chart(owner_fig, use_container_width=True)

    # DEALS TABLE
    page_heading(
        "Deals",
        "View open deals or include closed deals"
    )

    show_closed = st.toggle(
        "Show closed deals",
        value=True
    )

    display_deals = (
        filtered_deals.copy()
        if show_closed
        else open_deals.copy()
    )

    display_deals = display_deals.sort_values(
        "Expected close"
    )

    st.caption(f"{len(display_deals)} deals")

    st.dataframe(
        display_deals[
            [
                "Account", "Stage", "Amount", "Probability",
                "Weighted", "Expected close", "Owner",
                "Source", "Plan", "Region"
            ]
        ],
        hide_index=True,
        use_container_width=True,
        height=450
    )

    st.download_button(
        "📥 Download Deals",
        data=display_deals.to_csv(index=False).encode("utf-8"),
        file_name="deals.csv",
        mime="text/csv"
    )


# FOOTER
st.divider()
st.caption(
    "Nimbus BI Dashboard | Built with Python, Streamlit, Pandas and Plotly"
)
st.caption(
    "Note: This dashboard uses randomly generated sample data. "
    "Some business KPIs and charts are illustrative."
)