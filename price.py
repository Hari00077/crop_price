import streamlit as st
import pickle

st.title("Average crop Type price per Quintal in 2023")
# Load the model (assuming it's a DataFrame stored as a pickle file)
model = pickle.load(open("price.pkl", "rb"))

# Select state
state = st.selectbox("Select the state", model["State"].unique())

# Filter districts based on the selected state
filtered_df = model[model['State'] == state]
districts = st.selectbox("Select the district", filtered_df["District"].unique())

# Filter markets based on the selected district
new_df = model[model["District"] == districts]
Market = st.selectbox("Select market", new_df["Market"].unique())

# Filter commodities based on the selected market
Type_df = model[model["Market"] == Market]
Type = st.selectbox("Select_type", Type_df["Commodity"].unique())

# Filter minimum price based on the selected commodity
Min_df = model[model["Commodity"] == Type]
Min = Min_df["Min_x0020_Price"]
Max=Min_df["Max_x0020_Price"]

# Calculate the average of minimum prices
average_min_price = Min.mean()
avearge_max_price=Max.mean()

# Display the result when the button is clicked
if st.button("click"):
    st.write(f"The average minimum price for {Type} in {Market} is: {average_min_price}")
    st.write(f"The average maximum price for {Type} in {Market} is :{avearge_max_price}")
