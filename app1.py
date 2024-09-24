from flask import Flask, render_template, request
import pickle
import os
import pandas as pd

app = Flask(__name__)


# Load the price data
def load_data():
    try:
        if os.path.exists("price.pkl"):
            model = pickle.load(open("price.pkl", "rb"))
            return model
        else:
            raise FileNotFoundError("Price data file not found!")
    except Exception as e:
        raise Exception(f"Error loading the price data: {e}")


# Homepage route
@app.route("/", methods=["GET", "POST"])
def index():
    # Load the data
    model = load_data()

    # Initialize default values
    state = district = market = commodity = None
    average_min_price = average_max_price = None

    if request.method == "POST":
        # Get selected values from the form
        state = request.form.get("state")
        district = request.form.get("district")
        market = request.form.get("market")
        commodity = request.form.get("commodity")

        # Filter the data based on selections
        filtered_df = model[model['State'] == state]
        new_df = filtered_df[filtered_df["District"] == district]
        Type_df = new_df[new_df["Market"] == market]
        Min_df = Type_df[Type_df["Commodity"] == commodity]

        # Calculate the average prices
        average_min_price = Min_df["Min_x0020_Price"].mean()
        average_max_price = Min_df["Max_x0020_Price"].mean()

    # Get unique values for the dropdowns
    states = model["State"].unique() if model is not None else []
    districts = model[model['State'] == state]["District"].unique() if state else []
    markets = model[model["District"] == district]["Market"].unique() if district else []
    commodities = model[model["Market"] == market]["Commodity"].unique() if market else []

    return render_template(
        "index.html",
        states=states,
        districts=districts,
        markets=markets,
        commodities=commodities,
        selected_state=state,
        selected_district=district,
        selected_market=market,
        selected_commodity=commodity,
        average_min_price=average_min_price,
        average_max_price=average_max_price
    )


if __name__ == "__main__":
    app.run(debug=True)
