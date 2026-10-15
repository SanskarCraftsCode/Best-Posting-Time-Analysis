# Best Posting Time Analysis — Social Media Analytics

A working mini-project dashboard built with Python, Streamlit, Pandas and Plotly.

## Features
- Filter posts by social platform and weekday
- Compare average engagement rate, engagements, reach or clicks
- Charts for posting hour, day of week and platform
- Day × hour heatmap
- Top five posting windows (requires at least two posts in a window)
- View and download filtered post data

## Run locally
1. Install Python 3.10 or newer.
2. Extract this ZIP and open a terminal in the project folder.
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Start the dashboard:
   ```bash
   streamlit run app.py
   ```
5. Open the local URL Streamlit displays (usually `http://localhost:8501`).

## Dataset
`sample_posts.csv` contains synthetic demonstration data. Do not present its findings as real audience behaviour. Replace it with your exported analytics data while keeping these columns:
`post_id,date,platform,day,hour,likes,comments,shares,reach,clicks`

- `date`: YYYY-MM-DD
- `day`: full weekday name (Monday, Tuesday, ...)
- `hour`: 0–23 (local time zone for the account/audience)
- Counts: non-negative numeric values

For a meaningful analysis, collect several weeks of posts and avoid drawing conclusions from very small samples.

## Methodology
- Engagements = likes + comments + shares
- Engagement rate = engagements / reach × 100
- Aggregates performance by hour, day and platform
- Ranks day/hour combinations that have at least two observed posts

## Academic project summary
**Objective:** Identify posting periods associated with stronger social engagement using historical post-performance data.

**Problem statement:** Posting without analysing audience response can waste content opportunities. This dashboard compares performance across posting times to help creators form data-driven scheduling hypotheses.

**Tools:** Python, Streamlit, Pandas, Plotly, CSV.

**Limitation:** Correlation does not prove posting time caused performance. Content type, audience size, paid promotion, topic, and platform algorithms may influence results. Validate recommendations with controlled tests and real account data.
