import streamlit as st
import datetime
from datetime import datetime, timedelta
import pandas as pd
import random

st.set_page_config(page_title="YVR → BKK Premium Deals", layout="wide")

# Custom CSS for Background and UI Styling
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .metric-card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        text-align: center;
    }
    .flight-card {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.03);
    }
    </style>
""", unsafe_with_html=True)

st.title("✈️ YVR to BKK Flight Deals Finder")
st.sidebar.header("Search Settings")
st.sidebar.info("💡 Running in Premium Demo mode. No API key required!")

days_ahead = st.sidebar.slider("Search next X days", 7, 60, 30)
max_price = st.sidebar.number_input("Max price (CAD)", value=1500, step=50)
adults = st.sidebar.number_input("Adults", 1, 5, 1)
round_trip = st.sidebar.checkbox("Round trip", value=False)

return_days = 14
if round_trip:
    return_days = st.sidebar.slider("Return after X days", 7, 90, 14)

search_button = st.sidebar.button("🔍 Search Best Deals", type="primary")

# Simulates flight data locally with airline logo support
def generate_mock_deals(days_ahead, max_price, round_trip, return_days):
    today = datetime.now().date()
    deals = []
    
    # Dictionary linking airline codes to public logo assets
    airlines_pool = {
        "AC": "Air Canada",
        "NH": "ANA",
        "BR": "EVA Air",
        "CI": "China Airlines",
        "CX": "Cathay Pacific",
        "SQ": "Singapore Airlines"
    }
    
    for i in range(days_ahead):
        dep_date = today + timedelta(days=i)
        num_offers = random.randint(1, 3)
        
        for _ in range(num_offers):
            base_price = 850 if not round_trip else 1200
            day_variance = random.randint(-150, 450)
            price = base_price + day_variance
            
            if price > max_price:
                continue
                
            stops = random.choice([0, 1, 2])
            duration_hours = random.randint(16, 28)
            duration_mins = random.choice([0, 15, 30, 45])
            
            carrier_code = random.choice(list(airlines_pool.keys()))
            carrier_name = airlines_pool[carrier_code]
            
            dep_date_str = dep_date.strftime("%Y-%m-%d")
            # Clearbit API provides free instant logos by domain name
            logo_url = f"https://clearbit.com{carrier_name.lower().replace(' ', '')}.com"
            flight_url = f"https://google.com{dep_date_str}"
            
            deals.append({
                "Date": pd.to_datetime(dep_date),
                "Price (CAD)": float(round(price, 2)),
                "Stops": stops,
                "Duration": f"{duration_hours}h {duration_mins}m",
                "Airline Code": carrier_code,
                "Airline": carrier_name,
                "Logo": logo_url,
                "Link": flight_url
            })
    return deals

if "flight_deals" not in st.session_state:
    st.session_state.flight_deals = None

if search_button:
    with st.spinner("Generating premium flight schedules..."):
        deals = generate_mock_deals(days_ahead, max_price, round_trip, return_days)
        if deals:
            st.session_state.flight_deals = pd.DataFrame(deals).sort_values("Price (CAD)")
        else:
            st.session_state.flight_deals = pd.DataFrame()
            st.warning("No deals found matching criteria.")

# Render UI Filters, Summary Cards, and Clickable Image Tables
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
        # High-level overview metrics
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("Lowest Price Found", f"${filtered['Price (CAD)'].min():,.2f} CAD")
        with m2:
            st.metric("Average Deal Price", f"${filtered['Price (CAD)'].mean():,.2f} CAD")
        with m3:
            st.metric("Total Flight Options", len(filtered))

        st.subheader("📈 Price Trend")
        trend = filtered.groupby("Date")["Price (CAD)"].agg(["min", "mean"]).reset_index()
        trend.columns = ["Date", "Lowest Price", "Average Price"]
        st.line_chart(trend.set_index("Date"), use_container_width=True)

        st.subheader("✨ Available Deals (Click Carrier Logo to Book)")
        
        # Format Date Column for nicer presentation
        display_df = filtered.copy()
        display_df["Date"] = display_df["Date"].dt.strftime("%b %d, %Y")
        
        # Use Streamlit Column Config to transform text URLs into clickable images
        st.dataframe(
            display_df[["Logo", "Airline", "Date", "Price (CAD)", "Stops", "Duration"]], 
            use_container_width=True, 
            hide_index=True,
            column_config={
                "Logo": st.column_config.ImageColumn("Click to Book", help="Click on the logo to view flight details"),
                "Price (CAD)": st.column_config.NumberColumn("Price", format="$%.2f CAD")
            }
        )
    else:
        st.info("No rows match the selected UI filters.")

elif st.session_state.flight_deals is not None and st.session_state.flight_deals.empty:
    st.info("No flights matched your budget parameters.")
else:
    st.info("Tap the 'Search Best Deals' button in the sidebar to generate data.")

st.caption("YVR → BKK Flight Deals App (Visual Demo Mode)")
