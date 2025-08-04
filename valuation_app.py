import streamlit as st
import pandas as pd

st.set_page_config(page_title="Company Valuation Toolkit", layout="centered")

st.title("📊 Company Valuation Toolkit")
st.write("Estimate a company's fair value using DCF and Comparable Company Analysis.")

# Sidebar inputs
st.sidebar.header("Input Parameters")
company_name = st.sidebar.text_input("Company Name", "ABC Corp")
revenue = st.sidebar.number_input("Annual Revenue (in millions)", min_value=0.0, value=100.0, step=1.0)
ebitda_margin = st.sidebar.slider("EBITDA Margin (%)", 0.0, 100.0, 25.0)
growth_rate = st.sidebar.slider("Revenue Growth Rate (%)", 0.0, 50.0, 10.0)
discount_rate = st.sidebar.slider("Discount Rate / WACC (%)", 1.0, 20.0, 9.0)
terminal_growth = st.sidebar.slider("Terminal Growth Rate (%)", 0.0, 10.0, 3.0)
ev_ebitda_multiple = st.sidebar.slider("EV/EBITDA Multiple", 1.0, 30.0, 12.0)
years = 5

# Convert percentages to decimals
ebitda_margin /= 100
growth_rate /= 100
discount_rate /= 100
terminal_growth /= 100

# Create projection DataFrame
projection = pd.DataFrame(columns=["Year", "Revenue (M)", "EBITDA (M)", "Discounted EBITDA (M)"])

for year in range(1, years + 1):
    future_revenue = revenue * ((1 + growth_rate) ** year)
    future_ebitda = future_revenue * ebitda_margin
    discounted_ebitda = future_ebitda / ((1 + discount_rate) ** year)
    projection.loc[year - 1] = [f"Year {year}", future_revenue, future_ebitda, discounted_ebitda]

# Terminal value calculation
last_year_ebitda = projection["EBITDA (M)"].iloc[-1]
terminal_value = (last_year_ebitda * (1 + terminal_growth)) / (discount_rate - terminal_growth)
terminal_value_discounted = terminal_value / ((1 + discount_rate) ** years)

# Valuations
dcf_valuation = projection["Discounted EBITDA (M)"].sum() + terminal_value_discounted
current_ebitda = revenue * ebitda_margin
comps_valuation = current_ebitda * ev_ebitda_multiple
average_valuation = (dcf_valuation + comps_valuation) / 2
valuation_range = (min(dcf_valuation, comps_valuation), max(dcf_valuation, comps_valuation))

# Display results
st.header(f"Valuation Summary: {company_name}")
st.metric("Current Revenue", f"${revenue:.2f}M")
st.metric("Current EBITDA", f"${current_ebitda:.2f}M")

st.subheader("📈 5-Year DCF Projection")
st.dataframe(projection.style.format({
    "Revenue (M)": "${:,.2f}",
    "EBITDA (M)": "${:,.2f}",
    "Discounted EBITDA (M)": "${:,.2f}"
}))

st.subheader("📊 Valuation Results")
st.write(f"**Discounted Cash Flow (DCF) Valuation:** ${dcf_valuation:,.2f}M")
st.write(f"**Comparable Company (EV/EBITDA) Valuation:** ${comps_valuation:,.2f}M")
st.write(f"**Terminal Value (Discounted):** ${terminal_value_discounted:,.2f}M")
st.write(f"**Estimated Fair Value Range:** ${valuation_range[0]:,.2f}M - ${valuation_range[1]:,.2f}M")
st.success(f"**Average Valuation:** ${average_valuation:,.2f}M")
