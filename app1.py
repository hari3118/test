import streamlit as st
from breeze_connect import BreezeConnect
import pandas as pd
import io

# List of email IDs made by admin
admin_email_ids = ["admin@example.com", "admin2@example.com", "admin3@example.com"]

# Streamlit app code
def main():
    st.title("Stocks Data App")
    
    # Authentication section
    st.header("User Authentication")
    
    # Ask user for input
    user_email = st.text_input("Enter your email ID")

    # Check if the user's email matches any of the admin email IDs
    if user_email in admin_email_ids:
        st.success("Email ID validated successfully!")

        # Fetch customer details section
        st.header("Fetch Customer Details")

        # User input form for customer details
        with st.form("customer_details_form"):
            api_key = st.text_input("API Key")
            api_secret = st.text_input("API Secret")
            api_session = st.text_input("API Session")

            fetch_customer_details_button = st.form_submit_button(label="Fetch Customer Details")

        # Fetch and display customer details
        if fetch_customer_details_button:
            customer_details = get_customer_details(api_key, api_secret, api_session)
            idirect_userid = customer_details['Success']['idirect_userid']
            idirect_user_name = customer_details['Success']['idirect_user_name']

            st.subheader("Customer Details")
            st.write("IDirect User ID:", idirect_userid)
            st.write("IDirect User Name:", idirect_user_name)

        # Fetch stocks data section
        st.header("Fetch Stocks Data")

        # User input form for stock details
        with st.form("stocks_data_form"):
            interval = st.selectbox("Interval", ["1minute", "5minute", "30minute", "1day"])
            from_date = st.date_input("From Date")
            to_date = st.date_input("To Date")
            stock_code = st.text_input("Stock Code")
            expiry_date = st.date_input("Expiry Date")
            right = st.selectbox("Right", ["call", "put"])
            strike_price = st.text_input("Strike Price")

            fetch_stocks_data_button = st.form_submit_button(label="Fetch Stocks Data")

        # Fetch and display stocks data
        if fetch_stocks_data_button:
            df = get_historical_data(api_key, api_secret, api_session, interval, str(from_date), str(to_date), stock_code, str(expiry_date), right, strike_price)
            df = pd.DataFrame(df['Success'])
            df = df[['datetime', 'open', 'high', 'low', 'close', 'volume']]
            df = df.rename(columns={'datetime': 'time'})

            st.subheader("Stocks Data")
            st.write(df.head())

            # Create a BytesIO buffer
            buffer = io.BytesIO()
            df.to_csv(buffer, index=False)

            # Download button
            st.download_button(
                label="Download CSV",
                data=buffer.getvalue(),
                file_name="data.csv",
                mime="text/csv"
            )

    else:
        st.error("Email ID validation failed!")

def get_customer_details(api_key, api_secret, api_session):
    # Create an instance of BreezeConnect
    breeze = BreezeConnect(api_key=api_key)

    # Generate the session
    breeze.generate_session(api_secret=api_secret, session_token=api_session)

    # Fetch the customer details
    customer_details = breeze.get_customer_details(api_session=api_session)

    return customer_details

def get_historical_data(api_key, api_secret, api_session, interval, from_date, to_date, stock_code, expiry_date, right, strike_price):
    # Create an instance of BreezeConnect
    breeze = BreezeConnect(api_key=api_key)

    # Generate the session
    breeze.generate_session(api_secret=api_secret, session_token=api_session)

    # Fetch historical data
    df = breeze.get_historical_data(
        interval=interval,
        from_date=from_date,
        to_date=to_date,
        stock_code=stock_code,
        exchange_code="NFO",
        product_type="options",
        expiry_date=expiry_date,
        right=right,
        strike_price=strike_price
    )

    return df

if __name__ == "__main__":
    main()