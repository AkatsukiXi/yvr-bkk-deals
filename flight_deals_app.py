import streamlit as st
import datetime
from datetime import datetime, timedelta
import pandas as pd
import random

st.set_page_config(page_title="Agoda Flight Deals | YVR → BKK", layout="wide", initial_sidebar_state="collapsed")

# Agoda Brand Theme CSS Injection using safe native st.html
st.html("""
    <style>
    .stApp {
        background-color: #f8f9fa !important;
    }
    .hero-banner {
        background: linear-gradient(135deg, #2a2a2e 0%, #1a1a1c 100%);
        padding: 40px;
        border-radius: 16px;
        color: white;
        margin-bottom: 25px;
        text-align: center;
    }
    div[data-testid="stVerticalBimport streamlit as st
import datetime
from datetime import datetime, timedelta
import pandas as pd
import random

st.set_page_config(page_title="Cris Flight Deals | YVR → BKK", layout="wide", initial_sidebar_state="collapsed")

# Cris Flight Deals Brand Theme CSS Injection using safe native st.html
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

# Top Branding Banner using safe native st.html
st.html("""
    <div class="hero-banner">
        <h1 style="color: white; margin: 0; font-family: sans-serif;">Cris <span style="font-weight: 300; font-size: 24px;">flight deals</span></h1>
        <p style="color: #e0e0e0; margin-top: 5px; font-family: sans-serif;">Compare top-rated airlines from Vancouver to Bangkok</p>
    </div>
""")

# Main Horizontal Search Bar
search_box = st.container(border=True)
with search_box:
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        origin = st.text_input("🛫 Flying from", value="Vancouver (YVR)", disabled=True)
    with c2:
        destination = st.text_input("🛬 Flying to", value="Bangkok (BKK)", disabled=True)
    with c3:
        search_days = st.slider("📅 Search Window (Days Ahead)", 7, 60, 30)
    with c4:
        st.text("") 
        search_button = st.button("Search Deals", type="primary", use_container_width=True)

# Secondary Dynamic Sidebar Filters
st.sidebar.header("Filter Results")
max_price = st.sidebar.slider("Max Budget (CAD)", 800, 2500, 1600, step=50)
selected_stops = st.sidebar.multiselect("Stops", options=[0, 1, 2], default=[0, 1, 2])
sort_by = st.sidebar.radio("Sort Results By", ["Cheapest Price", "Shortest Duration"])

def generate_mock_deals(days_ahead, max_price):
    today = datetime.now().date()
    deals = []
    
    airlines_pool = {
        "AC": {"name": "Air Canada", "url": "https://clearbit.com", "rating": "4.2/5 Good"},
        "NH": {"name": "ANA All Nippon Airways", "url": "https://clearbit.com", "rating": "4.8/5 Excellent"},
        "BR": {"name": "EVA Air", "url": "https://clearbit.com", "rating": "4.7/5 Excellent"},
        "CX": {"name": "Cathay Pacific", "url": "https://clearbit.com", "rating": "4.5/5 Excellent"},
        "SQ": {"name": "Singapore Airlines", "url": "https://clearbit.com", "rating": "4.9/5 Top Choice"}
    }
    
    for i in range(days_ahead):
        dep_date = today + timedelta(days=i)
        num_offers = random.randint(1, 2)
        
        for _ in range(num_offers):
            price = random.randint(850, 1950)
            if price > max_price:
                continue
                
            stops = random.choice([0, 1, 2])
            duration_hours = random.randint(15, 26)
            duration_mins = random.choice([0, 15, 30, 45])
            
            carrier_code = random.choice(list(airlines_pool.keys()))
            carrier_data = airlines_pool[carrier_code]
            
            dep_date_str = dep_date.strftime("%Y-%m-%d")
            flight_url = f"https://google.com{dep_date_str}"
            
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

if "cris_deals" not in st.session_state:
    st.session_state.cris_deals = None

if search_button or st.session_state.cris_deals is None:
    with st.spinner("Fetching today's top flight rates..."):
        raw_deals = generate_mock_deals(search_days, max_price)
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
        
        st.subheader("💡 Today's Top Recommendations")
        
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
else:
    st.info("Adjust the top parameters and hit search to load flights.")
        box-shadow: 0 4px 12px rgba(0,0,0,0.03) !important;
        margin-bottom: 15px !important;
    }
    .agoda-badge {
        background-color: #e1f5fe;
        color: #0288d1;
        padding: 6px 12px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 13px;
        display: inline-block;
    }
    </style>
""")

# Top Agoda Branding Banner using safe native st.html
st.html("""
    <div class="hero-banner">
        <h1 style="color: white; margin: 0; font-family: sans-serif;">agoda <span style="font-weight: 300; font-size: 24px;">flight deals</span></h1>
        <p style="color: #a1a1a8; margin-top: 5px; font-family: sans-serif;">Compare top-rated airlines from Vancouver to Bangkok</p>
    </div>
""")

# Main Horizontal Search Bar (Agoda Pattern)
search_box = st.container(border=True)
with search_box:
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        origin = st.text_input("🛫 Flying from", value="Vancouver (YVR)", disabled=True)
    with c2:
        destination = st.text_input("🛬 Flying to", value="Bangkok (BKK)", disabled=True)
    with c3:
        search_days = st.slider("📅 Search Window (Days Ahead)", 7, 60, 30)
    with c4:
        st.markdown("<div style='height: 28px;'></div>", unsafe_with_html=True)
        search_button = st.button("Search Deals", type="primary", use_container_width=True)

# Secondary Dynamic Sidebar Filters
st.sidebar.header("Filter Results")
max_price = st.sidebar.slider("Max Budget (CAD)", 800, 2500, 1600, step=50)
selected_stops = st.sidebar.multiselect("Stops", options=[0, 1, 2], default=[0, 1, 2])
sort_by = st.sidebar.radio("Sort Results By", ["Cheapest Price", "Shortest Duration"])

def generate_mock_deals(days_ahead, max_price):
    today = datetime.now().date()
    deals = []
    
    airlines_pool = {
        "AC": {"name": "Air Canada", "url": "https://clearbit.com", "rating": "4.2/5 Good"},
        "NH": {"name": "ANA All Nippon Airways", "url": "https://clearbit.com", "rating": "4.8/5 Excellent"},
        "BR": {"name": "EVA Air", "url": "https://clearbit.com", "rating": "4.7/5 Excellent"},
        "CX": {"name": "Cathay Pacific", "url": "https://clearbit.com", "rating": "4.5/5 Excellent"},
        "SQ": {"name": "Singapore Airlines", "url": "https://clearbit.com", "rating": "4.9/5 Top Choice"}
    }
    
    for i in range(days_ahead):
        dep_date = today + timedelta(days=i)
        num_offers = random.randint(1, 2)
        
        for _ in range(num_offers):
            price = random.randint(850, 1950)
            if price > max_price:
                continue
                
            stops = random.choice([0, 1, 2])
            duration_hours = random.randint(15, 26)
            duration_mins = random.choice([0, 15, 30, 45])
            
            carrier_code = random.choice(list(airlines_pool.keys()))
            carrier_data = airlines_pool[carrier_code]
            
            dep_date_str = dep_date.strftime("%Y-%m-%d")
            flight_url = f"https://google.com{dep_date_str}"
            
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

if "agoda_deals" not in st.session_state:
    st.session_state.agoda_deals = None

if search_button or st.session_state.agoda_deals is None:
    with st.spinner("Fetching today's top agoda flight rates..."):
        raw_deals = generate_mock_deals(search_days, max_price)
        st.session_state.agoda_deals = pd.DataFrame(raw_deals)

df = st.session_state.agoda_deals

if df is not None and not df.empty:
    filtered_df = df[(df["Stops"].isin(selected_stops)) & (df["Price"] <= max_price)]
    
    if sort_by == "Cheapest Price":
        filtered_df = filtered_df.sort_values("Price", ascending=True)
    else:
        filtered_df = filtered_df.sort_values("DurationHours", ascending=True)

    if not filtered_df.empty:
        cheapest_price = filtered_df["Price"].min()
        
        st.subheader("💡 Today's Top Recommendations")
        
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
                    st.markdown(f"<h2 style='margin:0; color:#111; font-family:sans-serif;'>${row['Price']} <span style='font-size:14px; color:#666;'>CAD</span></h2>", unsafe_with_html=True)
                    st.link_button("Book Deal ➔", row["Link"], type="primary", use_container_width=True)
    else:
        st.info("No matching flights found for the active filter parameters.")
else:
    st.info("Adjust the top parameters and hit search to load flights.")
