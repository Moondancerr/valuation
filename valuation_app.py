import pandas as pd

# --- Step 1: Inputs ---
company_name = input("Enter company name: ")

# Key financial inputs
revenue = float(input("Enter current annual revenue (in millions): "))
ebitda_margin = float(input("Enter EBITDA margin (as %): ")) / 100
growth_rate = float(input("Enter annual revenue growth rate (as %): ")) / 100
discount_rate = float(input("Enter discount rate / WACC (as %): ")) / 100
terminal_growth = float(input("Enter terminal growth rate (as %): ")) / 100
ev_ebitda_multiple = float(input("Enter industry EV/EBITDA multiple: "))
years = 5

# --- Step 2: Build Projection DataFrame ---
projection = pd.DataFrame(columns=["Year", "Revenue", "EBITDA", "Discounted EBITDA"])

for year in range(1, years + 1):
    projected_revenue = revenue * ((1 + growth_rate) ** year)
    projected_ebitda = projected_revenue * ebitda_margin
    discounted_ebitda = projected_ebitda / ((1 + discount_rate) ** year)

    projection.loc[year - 1] = [f"Year {year}", projected_revenue, projected_ebitda, discounted_ebitda]

# --- Step 3: Terminal Value ---
last_year_ebitda = projection["EBITDA"].iloc[-1]
terminal_value = (last_year_ebitda * (1 + terminal_growth)) / (discount_rate - terminal_growth)
terminal_value_discounted = terminal_value / ((1 + discount_rate) ** years)

# --- Step 4: Valuation Calculations ---
dcf_valuation = projection["Discounted EBITDA"].sum() + terminal_value_discounted
current_ebitda = revenue * ebitda_margin
comps_valuation = current_ebitda * ev_ebitda_multiple
average_valuation = (dcf_valuation + comps_valuation) / 2

# --- Step 5: Output ---
print(f"\n--- Valuation Summary for {company_name} ---")
print(f"Current Revenue: ${revenue:.2f}M")
print(f"Current EBITDA: ${current_ebitda:.2f}M")

print("\n--- 5-Year DCF Projection ---")
print(projection.round(2).to_string(index=False))

print(f"\nTerminal Value (Discounted): ${terminal_value_discounted:.2f}M")
print(f"DCF Valuation: ${dcf_valuation:.2f}M")
print(f"Comparable Valuation (EV/EBITDA): ${comps_valuation:.2f}M")
print(f"\nEstimated Fair Value Range: ${min(dcf_valuation, comps_valuation):.2f}M - ${max(dcf_valuation, comps_valuation):.2f}M")
print(f"Average Valuation: ${average_valuation:.2f}M")
