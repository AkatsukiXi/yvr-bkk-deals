import streamlit as st
import datetime
from datetime import datetime, timedelta
import pandas as pd
import random

st.set_page_config(page_title="Cris Flight Deals | Global Search", layout="wide", initial_sidebar_state="collapsed")

# Cris Flight Deals Brand Theme CSS Injection
st.html("""
    <style>
    .stApp {
        background-color: #f8f9fa !important;
    }
    .hero-banner {
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        padding: 40px;
        border-radius: 16px;
        color: white;
        margin-bottom: 25px;
        text-align: center;
    }
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: white !important;
        border: 1px solid #e4e4e4 !important;
        border-radius: 12px !important;
        padding: 20px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03) !important;
        margin-bottom: 15px !important;
    }
    .cris-badge {
        background-color: #e1f5fe;
        color: #0288d1;
        padding: 6px 12px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 13px;
        display: inline-block;
    }
    .cris-price {
        font-size: 28px;
        font-weight: bold;
        color: #111111;
        font-family: sans-serif;
        margin: 0;
    }
    .cris-currency {
        font-size: 14px;
        color: #666666;
        font-weight: normal;
    }
    </style>
""")

# Top Branding Banner
st.html("""
    <div class="hero-banner">
        <h1 style="color: white; margin: 0; font-family: sans-serif;">Cris <span style="font-weight: 300; font-size: 24px;">flight deals</span></h1>
        <p style="color: #e0e0e0; margin-top: 5px; font-family: sans-serif;">Find custom real-time simulated flight deals worldwide</p>
    </div>
""")

# Airport Dictionary Database (Major global hubs across continents)
airports = {
    "YVR - Vancouver International Airport": "YVR",
    "YYZ - Toronto Pearson International Airport": "YYZ",
    "LAX - Los Angeles International Airport": "LAX",
    "JFK - John F. Kennedy International Airport (New York)": "JFK",
    "LHR - London Heathrow Airport": "LHR",
    "CDG - Paris Charles de Gaulle Airport": "CDG",
    "HND - Tokyo Haneda Airport": "HND",
    "NRT - Tokyo Narita Airport": "NRT",
    "BKK - Suvarnabhumi Airport (Bangkok)": "BKK",
    "SIN - Singapore Changi Airport": "SIN",
    "HKG - Hong Kong International Airport": "HKG",
    "SYD - Sydney Kingsford Smith Airport": "SYD",
    "DXB - Dubai International Airport": "DXB",
    "FRA - Frankfurt Airport": "FRA",
    "AMS - Amsterdam Airport Schiphol": "AMS",
    "ICN - Seoul Incheon International Airport": "ICN",
}

# Main Horizontal Search Bar
search_box = st.container(border=True)
with search_box:
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        # Dropdown selection for Origin Airport
        origin_label = st.selectbox("🛫 Flying from", options=list(airports.keys()), index=0)
        origin_code = airports[origin_label]
    with c2:
        # Dropdown selection for Destination Airport (defaults to Bangkok)
        dest_label = st.selectbox("🛬 Flying to", options=list(airports.keys()), index=8)
        dest_code = airports[dest_label]
    with c3:
        search_days = st.slider("📅 Search Window (Days Ahead)", 7, 60, 30)
    with c4:
        st.text("") 
        search_button = st.button("Search Deals", type="primary", use_container_width=True)

# Secondary Dynamic Sidebar Filters
st.sidebar.header("Filter Results")
max_price = st.sidebar.slider("Max Budget (CAD)", 400, 3500, 1600, step=50)
selected_stops = st.sidebar.multiselect("Stops", options=, default=)
sort_by = st.sidebar.radio("Sort Results By", ["Cheapest Price", "Shortest Duration"])

def generate_mock_deals(days_ahead, max_price, origin, destination):
    # Quick protection check to avoid generating loops to identical locations
    if origin == destination:
        return []
        
    today = datetime.now().date()
    deals = []
    
    # Expanded global airline mix matching regional airport logic
    airlines_pool = {
        "AC": {"name": "Air Canada", "url": "https://clearbit.com", "rating": "4.2/5 Good"},
        "NH": {"name": "ANA All Nippon Airways", "url": "https://clearbit.com", "rating": "4.8/5 Excellent"},
        "BR": {"name": "EVA Air", "url": "https://clearbit.com", "rating": "4.7/5 Excellent"},
        "CX": {"name": "Cathay Pacific", "url": "https://clearbit.com", "rating": "4.5/5 Excellent"},
        "SQ": {"name": "Singapore Airlines", "url": "https://clearbit.com", "rating": "4.9/5 Top Choice"},
        "BA": {"name": "British Airways", "url": "https://clearbit.com", "rating": "4.0/5 Good"},
        "LH": {"name": "Lufthansa", "url": "https://clearbit.com", "rating": "4.3/5 Very Good"},
        "EK": {"name": "Emirates", "url": "https://clearbit.com", "rating": "4.7/5 Excellent"},
        "DL": {"name": "Delta Air Lines", "url": "https://clearbit.com", "rating": "4.1/5 Good"}
    }
    
    for i in range(days_ahead):
        dep_date = today + timedelta(days=i)
        num_offers = random.randint(1, 2)
        
        for _ in range(num_offers):
            # Dynamic price range estimation depending on whether routing requires a long haul
            price = random.randint(450, 2250)
            if price > max_price:
                continue
                
            stops = random.choice()
            duration_hours = random.randint(5, 28)
            duration_mins = random.choice()
            
            carrier_code = random.choice(list(airlines_pool.keys()))
            carrier_data = airlines_pool[carrier_code]
            
            dep_date_str = dep_date.strftime("%Y-%m-%d")
            # Dynamic Google Flights URL mapping using user selection airport codes
            flight_url = f"https://google.com{destination}%20from%20{origin}%20on%20{dep_date_str}"
            
            deals.append({
                "DateObj": dep_date,
                "Date": dep_date.strftime("%b %d, %Y"),
                "Price": price,
                "Stops": stops,
                "DurationHours": duration_hours,
                "Duration": f"{duration_hours}h {duration_mins}m",
                "Airline": carrier_data["name"],
                "Logo": carrier_data["url"],
                "Rating": carrier_data["rating"],
                "Link": flight_url
            })
    return deals

# Clear cache whenever a user queries new destinations to ensure clean grid switching
if "cris_deals" not in st.session_state or search_button:
    with st.spinner("Fetching custom routes and rates..."):
        raw_deals = generate_mock_deals(search_days, max_price, origin_code, dest_code)
        st.session_state.cris_deals = pd.DataFrame(raw_deals)

df = st.session_state.cris_deals

if df is not None and not df.empty:
    filtered_df = df[(df["Stops"].isin(selected_stops)) & (df["Price"] <= max_price)]
    
    if sort_by == "Cheapest Price":
        filtered_df = filtered_df.sort_values("Price", ascending=True)
    else:
        filtered_df = filtered_df.sort_values("DurationHours", ascending=True)

    if not filtered_df.empty:
        cheapest_price = filtered_df["Price"].min()
        
        st.subheader(f"💡 Top Recommendations from {origin_code} to {dest_code}")
        
        for idx, row in filtered_df.head(10).iterrows():
            with st.container():
                col_logo, col_info, col_stops, col_price = st.columns(4)
                
                with col_logo:
                    st.image(row["Logo"], width=65)
                    st.caption(row["Airline"])
                
                with col_info:
                    st.markdown(f"### 🗓️ {row['Date']}")
                    st.write(f"⭐ {row['Rating']}")
                
                with col_stops:
                    stops_text = "Direct Flight" if row["Stops"] == 0 else f"{row['Stops']} Stop(s)"
                    st.markdown(f"**Duration:** {row['Duration']}")
                    st.markdown(f"**Route:** {stops_text}")
                
                with col_price:
                    if row["Price"] == cheapest_price:
                        st.write("🔥 CHEAPEST DEAL")
                    st.html(f'<p class="cris-price">${row["Price"]} <span class="cris-currency">CAD</span></p>')
                    st.link_button("Book Deal ➔", row["Link"], type="primary", use_container_width=True)
    else:
        st.info("No matching flights found for the active filter parameters.")
elif origin_code == dest_code:
    st.error("Error: Origin and Destination airports cannot be the same. Please select different cities.")
else:
    st.info("Adjust the parameters above and hit search to calculate routes.")
