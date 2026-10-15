import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(page_title="Best Posting Time Analysis", page_icon="📊", layout="wide")
st.title("📊 Best Posting Time Analysis")
st.caption("Social Media Analytics mini-project | Discover when posts perform best")

DATA_PATH = Path(__file__).parent / "sample_posts.csv"

@st.cache_data
def load_data():
    return pd.read_csv(DATA_PATH)

def prepare(df):
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["hour"] = pd.to_numeric(df["hour"], errors="coerce")
    for col in ["likes", "comments", "shares", "reach", "clicks"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(0)
    df = df.dropna(subset=["date", "platform", "day", "hour"])
    df["engagements"] = df["likes"] + df["comments"] + df["shares"]
    safe_reach = df["reach"].where(df["reach"] != 0)
    df["engagement_rate"] = (df["engagements"] / safe_reach * 100).fillna(0)
    df["time_slot"] = df["hour"].astype(int).map(lambda h: f"{h:02d}:00")
    return df

df = prepare(load_data())
with st.sidebar:
    st.header("Filters")
    platforms = st.multiselect("Platform", sorted(df["platform"].unique()), default=sorted(df["platform"].unique()))
    days = st.multiselect("Day of week", ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],
                          default=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"])
    metric_label = st.selectbox("Performance metric", ["Engagement rate (%)", "Total engagements", "Reach", "Clicks"])
    metric_col = {"Engagement rate (%)":"engagement_rate", "Total engagements":"engagements",
                  "Reach":"reach", "Clicks":"clicks"}[metric_label]
    st.caption("Sample data is synthetic. Replace it with your exported post analytics for real recommendations.")

filtered = df[df["platform"].isin(platforms) & df["day"].isin(days)]
if filtered.empty:
    st.warning("No rows match these filters. Select at least one platform and day.")
    st.stop()

overall = filtered[metric_col].mean()
best_hour = filtered.groupby("hour")[metric_col].mean().idxmax()
best_day = filtered.groupby("day")[metric_col].mean().idxmax()
best_platform = filtered.groupby("platform")[metric_col].mean().idxmax()
c1,c2,c3,c4 = st.columns(4)
c1.metric("Posts analysed", f"{len(filtered):,}")
c2.metric("Best hour", f"{int(best_hour):02d}:00")
c3.metric("Best day", best_day)
c4.metric("Top platform", best_platform)

st.subheader("Performance by posting hour")
hourly = filtered.groupby("hour", as_index=False).agg(
    performance=(metric_col, "mean"), posts=("post_id", "count"))
hourly["time"] = hourly["hour"].astype(int).map(lambda h:f"{h:02d}:00")
fig = px.bar(hourly, x="time", y="performance", hover_data=["posts"],
             labels={"time":"Posting time","performance":f"Average {metric_label}"},
             title=f"Average {metric_label} by hour")
fig.update_layout(xaxis={"categoryorder":"array","categoryarray":[f"{h:02d}:00" for h in range(24)]})
st.plotly_chart(fig, use_container_width=True)

left,right = st.columns(2)
with left:
    st.subheader("Day-of-week analysis")
    day_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    day_perf = filtered.groupby("day", as_index=False)[metric_col].mean()
    day_perf["day"] = pd.Categorical(day_perf["day"], categories=day_order, ordered=True)
    day_perf = day_perf.sort_values("day")
    st.plotly_chart(px.bar(day_perf, x="day", y=metric_col, labels={metric_col:f"Average {metric_label}"}),
                    use_container_width=True)
with right:
    st.subheader("Platform comparison")
    platform_perf = filtered.groupby("platform", as_index=False)[metric_col].mean().sort_values(metric_col, ascending=False)
    st.plotly_chart(px.bar(platform_perf, x="platform", y=metric_col, color="platform",
                           labels={metric_col:f"Average {metric_label}"}), use_container_width=True,
                    )

st.subheader("Day × hour heatmap")
heat = filtered.pivot_table(index="day", columns="hour", values=metric_col, aggfunc="mean")
heat = heat.reindex(day_order)
heat.columns = [f"{int(x):02d}:00" for x in heat.columns]
st.plotly_chart(px.imshow(heat, aspect="auto", labels=dict(x="Hour", y="Day", color=metric_label),
                          title=f"{metric_label}: day and hour"), use_container_width=True)

st.subheader("Recommended posting windows")
recommendations = (filtered.groupby(["day","hour"], as_index=False)
                   .agg(avg_performance=(metric_col,"mean"), post_count=("post_id","count"))
                   .query("post_count >= 2")
                   .sort_values("avg_performance", ascending=False).head(5))
if recommendations.empty:
    st.info("Not enough repeated observations for recommendations. Add more post records.")
else:
    recommendations["hour"] = recommendations["hour"].astype(int).map(lambda h:f"{h:02d}:00")
    recommendations = recommendations.rename(columns={"day":"Day","hour":"Time","avg_performance":f"Average {metric_label}","post_count":"Posts"})
    st.dataframe(recommendations, use_container_width=True, hide_index=True)

with st.expander("View filtered post data"):
    st.dataframe(filtered.sort_values("date", ascending=False), use_container_width=True, hide_index=True)

csv = filtered.to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download filtered data (CSV)", csv, "filtered_post_analytics.csv", "text/csv")
st.info("Interpretation tip: compare engagement rate as well as raw likes/reach. A high-performing time in this sample is a hypothesis to test, not a universal rule.")
