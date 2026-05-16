import streamlit as st
import requests
from datetime import datetime, timedelta
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

st.set_page_config(page_title="YVR → BKK Deals", layout="wide")
st.title("✈️ YVR to BKK Flight Deals Finder")

st.sidebar.header("Search Settings")

api_key = st.sidebar.text_input("Amadeus API Key", value="", type="password")
api_secret = st.sidebar.text_input("Amadeus API Secret", value="", type="password")

days_ahead = st.sidebar.slider("Search next X days", 7, 60, 30)
max_price = st.sidebar.number_input("Max price (CAD)", value=1500, step=50)
adults = st.sidebar.number_input("Adults", 1, 5, 1)
round_trip = st.sidebar.checkbox("Round trip", value=False)

if round_trip:
    return_days = st.sidebar.slider("Return after X days", 7, 90, 14)

search_button = st.sidebar.button("🔍 Search Best Deals", type="primary")

# Helper function to fetch single date to allow parallel execution
def fetch_date_deal(i, today, token, adults, round_trip, return_days, max_price):
    dep_date = (today + timedelta(days=i)).strftime("%Y-%m-%d")
    params = {
        "originLocationCode": "YVR",
        "destinationLocationCode": "BKK",
        "departureDate": dep_date,
        "adults": adults,
        "max": 5,
        "currencyCode": "CAD",
        "sort": "PRICE"
    }
    if round_trip:
        params["returnDate"] = (today + timedelta(days=i + return_days)).strftime("%Y-%m-%d")

    try:
        resp = requests.get(
            "https://test.api.amadeus.com/v2/shopping/flight-offers",
            headers={"Authorization": f"Bearer {token}"},
            params=params,
            timeout=10
        )
        if resp.status_code == 429:
            return "rate_limit"
        if resp.status_code != 200:
            return []
            
        day_deals = []
        for offer in resp.json().get("data", []):
            price = float(offer["price"]["total"])
            if price > max_price:
                continue
            itinerary = offer.get("itineraries", [{}])[0]
            segments = itinerary.get("segments", [])
            day_deals.append({
                "Date": pd.to_datetime(dep_date),
                "Price (CAD)": round(price, 2),
                "Stops": len(segments) - 1,
                "Duration": itinerary.get("duration", "N/A").replace("PT", ""),
                "Airlines": ", ".join(set(s.get("carrierCode", "") for s in segments)),
                "Link": f"https://www.google.com/travel/flights?q=Flights%20to%20BKK%20from%20YVR%20on%20{dep_date}"
            })
        return day_deals
    except Exception:
        return []

# Initialize session state for data persistence across filter changes
if "flight_deals" not in st.session_state:
    st.session_state.flight_deals = None

if search_button:
    if not api_key or not api_secret:
        st.error("Please enter your Amadeus API Key and Secret.")
        st.stop()

    with st.spinner("Searching flights concurrently..."):
        try:
            token_resp = requests.post(
                "https://test.api.amadeus.com/v1/security/oauth2/token",
                data={"grant_type": "client_credentials", "client_id": api_key, "client_secret": api_secret}
            )
            token_resp.raise_for_status()
            token = token_resp.json()["access_token"]

            today = datetime.now().date()
            deals = []
            
            # Use ThreadPoolExecutor to request dates in parallel (up to 5 threads to avoid spam block)
            with ThreadPoolExecutor(max_workers=5) as executor:
                futures = [
                    executor.submit(fetch_date_deal, i, today, token, adults, round_trip, return_days, max_price) 
                    for i in range(days_ahead)
                ]
                for future in futures:
                    res = future.result()
                    if res == "rate_limit":
                        st.warning("Amadeus API Rate limit hit. Try lowering the 'days ahead' range.")
                        break
                    if res:
                        deals.extend(res)

            if deals:
                st.session_state.flight_deals = pd.DataFrame(deals).sort_values("Price (CAD)")
            else:
                st.session_state.flight_deals = pd.DataFrame()
                st.warning("No deals found matching criteria.")

        except Exception as e:
            st.error(f"Authentication/Network Error: {e}")

# Render UI Controls & Charts if Data exists in Session State
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
    st.info("Enter your Amadeus API keys in the sidebar then tap Search")
    st.markdown("**Get free keys here:** [developers.amadeus.com](https://developers.amadeus.com)")

st.caption("YVR → BKK Flight Deals App")
