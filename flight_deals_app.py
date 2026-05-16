import streamlit as st
import datetime
from datetime import datetime, timedelta
import pandas as pd
import random

st.set_page_config(page_title="YVR → BKK Deals", layout="wide")
st.title("✈️ YVR to BKK Flight Deals Finder")

st.sidebar.header("Search Settings")
st.sidebar.info("💡 Running in Preview/Demo mode. No API key required!")

days_ahead = st.sidebar.slider("Search next X days", 7, 60, 30)
max_price = st.sidebar.number_input("Max price (CAD)", value=1500, step=50)
adults = st.sidebar.number_input("Adults", 1, 5, 1)
round_trip = st.sidebar.checkbox("Round trip", value=False)

# Local variable assignment to prevent scope errors if unchecked
return_days = 14
if round_trip:
    return_days = st.sidebar.slider("Return after X days", 7, 90, 14)

search_button = st.sidebar.button("🔍 Search Best Deals", type="primary")

# Simulates flight data locally without network calls
def generate_mock_deals(days_ahead, max_price, round_trip, return_days):
    today = datetime.now().date()
    deals = []
    airlines_pool = ["AC", "NH", "BR", "CI", "KE", "CX", "SQ"]
    
    for i in range(days_ahead):
        dep_date = today + timedelta(days=i)
        
        # Generate 1 to 3 random flight offers per day
        num_offers = random.randint(1, 3)
        for _ in range(num_offers):
            # Base price simulation logic
            base_price = 850 if not round_trip else 1200
            day_variance = random.randint(-150, 450)
            price = base_price + day_variance
            
            # Apply user's sidebar max price filter
            if price > max_price:
                continue
                
            stops = random.choice([1, 2])
            duration_hours = random.randint(16, 28)
            duration_mins = random.choice([0, 15, 30, 45])
            
            # Pick unique airlines for the legs
            sampled_airlines = random.sample(airlines_pool, k=stops + 1)
            
            dep_date_str = dep_date.strftime("%Y-%m-%d")
            deals.append({
                "Date": pd.to_datetime(dep_date),
                "Price (CAD)": float(round(price, 2)),
                "Stops": stops,
                "Duration": f"{duration_hours}H{duration_mins}M",
                "Airlines": ", ".join(sampled_airlines),
                "Link": f"https://www.google.com/travel/flights?q=Flights%20to%20BKK%20from%20YVR%20on%20{dep_date_str}"
            })
    return deals

# Session state management
if "flight_deals" not in st.session_state:
    st.session_state.flight_deals = None

if search_button:
    with st.spinner("Generating simulated flight schedules..."):
        deals = generate_mock_deals(days_ahead, max_price, round_trip, return_days)
        
        if deals:
            st.session_state.flight_deals = pd.DataFrame(deals).sort_values("Price (CAD)")
        else:
            st.session_state.flight_deals = pd.DataFrame()
            st.warning("No deals found matching criteria.")

# Render UI Filters & Charts
if st.session_state.flight_deals is not None and not st.session_state.flight_deals.empty:
    df = st.session_state.flight_deals

    st.subheader("⚡ Interactive Filters")
    col1, col2 = st.columns(2)
    with col1:
        selected_stops = st.multiselect("Filter by Stops", sorted(df["Stops"].unique()), default=sorted(df["Stops"].unique()))
    with col2:
        min_price = st.number_input("Minimum Budget Limit (CAD)", value=0, step=50)

    filtered = df[(df["Stops"].isin(selected_stops)) & (df["Price (CAD)"] >= min_price)]

    if not filtered.empty:
        st.subheader("📈 Price Trend")
        trend = filtered.groupby("Date")["Price (CAD)"].agg(["min", "mean"]).reset_index()
        trend.columns = ["Date", "Lowest Price", "Average Price"]
        st.line_chart(trend.set_index("Date"), use_container_width=True)

        st.subheader(f"Results ({len(filtered)} deals found)")
        st.dataframe(
            filtered, 
            use_container_width=True, 
            hide_index=True,
            column_config={"Link": st.column_config.LinkColumn("Book / Check Deal")}
        )
    else:
        st.info("No rows match the selected UI filters.")

elif st.session_state.flight_deals is not None and st.session_state.flight_deals.empty:
    st.info("No flights matched your budget parameters.")
else:
    st.info("Tap the 'Search Best Deals' button in the sidebar to generate data.")

st.caption("YVR → BKK Flight Deals App (Offline Demo Mode)")
