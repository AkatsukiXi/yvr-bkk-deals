import streamlit as st
import requests
from datetime import datetime, timedelta
import pandas as pd

st.set_page_config(page_title="YVR → BKK Deals", layout="wide")
st.title("✈️ YVR to BKK Flight Deals Finder")

st.sidebar.header("Search Settings")


days_ahead = st.sidebar.slider("Search next X days", 7, 60, 30)
max_price = st.sidebar.number_input("Max price (CAD)", value=1500, step=50)
adults = st.sidebar.number_input("Adults", 1, 5, 1)
round_trip = st.sidebar.checkbox("Round trip", value=False)

if round_trip:
    return_days = st.sidebar.slider("Return after X days", 7, 90, 14)

search_button = st.sidebar.button("🔍 Search Best Deals", type="primary")



    with st.spinner("Searching flights..."):
        try:
            token_resp = requests.post(
                "https://test.api.amadeus.com/v1/security/oauth2/token",
                data={"grant_type": "client_credentials", "client_id": api_key, "client_secret": api_secret}
            )
            token_resp.raise_for_status()
            token = token_resp.json()["access_token"]

            deals = []
            today = datetime.now().date()
            progress = st.progress(0)

            for i in range(days_ahead):
                dep_date = (today + timedelta(days=i)).strftime("%Y-%m-%d")
                progress.progress((i + 1) / days_ahead)

                params = {
                    "originLocationCode": "YVR",
                    "destinationLocationCode": "BKK",
                    "departureDate": dep_date,
                    "adults": adults,
                    "max": 10,
                    "currencyCode": "CAD",
                    "sort": "PRICE"
                }

                if round_trip:
                    ret_date = (today + timedelta(days=i + return_days)).strftime("%Y-%m-%d")
                    params["returnDate"] = ret_date

                resp = requests.get(
                    "https://test.api.amadeus.com/v2/shopping/flight-offers",
                    headers={"Authorization": f"Bearer {token}"},
                    params=params
                )

                if resp.status_code == 200:
                    for offer in resp.json().get("data", []):
                        price = float(offer["price"]["total"])
                        if price > max_price:
                            continue
                        itinerary = offer.get("itineraries", [{}])[0]
                        segments = itinerary.get("segments", [])
                        deal = {
                            "Date": pd.to_datetime(dep_date),
                            "Price (CAD)": round(price, 2),
                            "Stops": len(segments) - 1,
                            "Duration": itinerary.get("duration", "N/A"),
                            "Airlines": ", ".join(set(s.get("carrierCode", "") for s in segments)),
                            "Link": f"https://www.google.com/travel/flights?q=Flights%20to%20BKK%20from%20YVR%20on%20{dep_date}"
                        }
                        deals.append(deal)

            progress.empty()

            if not deals:
                st.warning("No deals found.")
                st.stop()

            df = pd.DataFrame(deals).sort_values("Price (CAD)")

            st.subheader("Filters")
            col1, col2 = st.columns(2)
            with col1:
                selected_stops = st.multiselect("Stops", sorted(df["Stops"].unique()), default=sorted(df["Stops"].unique()))
            with col2:
                min_price = st.number_input("Min Price (CAD)", value=0, step=50)

            filtered = df[(df["Stops"].isin(selected_stops)) & (df["Price (CAD)"] >= min_price)]

            st.subheader("📈 Price Trend")
            if not filtered.empty:
                trend = filtered.groupby("Date")["Price (CAD)"].agg(["min", "mean", "max"]).reset_index()
                trend.columns = ["Date", "Lowest", "Average", "Highest"]
                st.line_chart(trend.set_index("Date"), use_container_width=True)

            st.subheader(f"Results ({len(filtered)} deals)")
            st.dataframe(filtered, use_container_width=True, hide_index=True,
                        column_config={"Link": st.column_config.LinkColumn("Check Deal")})

        except Exception as e:
            st.error(f"Error: {e}")
else:
    st.info("Enter your Amadeus API keys in the sidebar then tap Search")
    st.markdown("**Get free keys here:** [developers.amadeus.com](https://developers.amadeus.com)")

st.caption("YVR → BKK Flight Deals App")
