import streamlit as st
import pandas as pd

# User Inputs
investment = st.number_input('Investment', value=4066700, format="%d")
equity_percent = st.number_input('Eigenkapital (%)', value=20.0) / 100.0
interest_rate = st.number_input('Zinssatz (%)', value=5.0) / 100.0
loan_duration = st.number_input('Laufzeit Kredit (Jahre)', value=5, format="%d")
depreciation = st.number_input('Abschreibung pro Jahr', value=508338, format="%d")
maintenance = st.number_input('Wartung', value=81334, format="%d")
insurance = st.number_input('Versicherung', value=40667, format="%d")
management = st.number_input('Geschäftsführung', value=50000, format="%d")
revenue = st.number_input('Einnahmen pro Jahr', value=1200000, format="%d")
tax_rate = st.number_input('Steuern (%)', value=30.0) / 100.0
project_duration = st.number_input('Projektlebenszeit (Jahre)', value=12, format="%d")

# Calculate Loan Amount automatically
loan_amount = round(investment * (1 - equity_percent))

# Calculate Annuity Payment
annuity_payment = round((loan_amount * interest_rate) / (1 - (1 + interest_rate) ** -loan_duration))

# Calculate equity (EK) in monetary terms
equity = round(investment * equity_percent)

# Calculations
years = range(1, project_duration + 1)
data = []

cumulative_tilgung = 0
remaining_loan = loan_amount
total_profit = 0

for year in years:
    # Umsatz
    umsatz = round(revenue)
    
    # Kosten
    kosten = round(maintenance + insurance + management)
    
    # Zinskosten (Interest part of the annuity)
    zinskosten = round(remaining_loan * interest_rate) if year <= loan_duration else 0
    
    # Tilgung (Repayment part of the annuity)
    tilgung = round(annuity_payment - zinskosten) if year <= loan_duration else 0
    cumulative_tilgung += tilgung
    
    # Rohertrag
    rohertrag = round(umsatz - kosten - zinskosten)
    
    # Ertrag vor Steuern
    ertrag_vor_steuern = round(rohertrag - depreciation)
    
    # Steuern (including Gewerbesteuer, Körperschaftsteuer, Soli)
    steuern = round(ertrag_vor_steuern * tax_rate)
    
    # Gewinn nach Steuern
    gewinn_nach_steuern = round(ertrag_vor_steuern - steuern)
    
    # Gewinn nach Steuern und Abschreibung
    gewinn_nach_steuern_und_abschreibung = round(gewinn_nach_steuern + depreciation - tilgung)
    
    # Accumulate total profit over the project duration
    total_profit += gewinn_nach_steuern_und_abschreibung
    
    # Update remaining loan after tilgung
    remaining_loan -= tilgung
    
    # Append row
    data.append([
        umsatz,
        kosten,
        zinskosten,
        rohertrag,
        depreciation,
        ertrag_vor_steuern,
        steuern,
        gewinn_nach_steuern,
        tilgung,
        cumulative_tilgung,
        gewinn_nach_steuern_und_abschreibung
    ])

# Convert to DataFrame
df = pd.DataFrame(data, columns=[
    "Umsatz",
    "Kosten",
    "Zinskosten",
    "Rohertrag",
    "Abschreibung",
    "Ertrag vor Steuern",
    "Steuern",
    "Gewinn nach Steuern",
    "Tilgung",
    "Tilgung kumuliiert",
    "Gewinn nach Steuern und Abschreibung"
], index=years)

# Effective annual return on equity (simple average)
effective_annual_return = (total_profit / (equity * project_duration)) * 100

# Display DataFrame
st.dataframe(df)

# Display total profit and effective annual return
st.write(f"**Total Absolute Profit over the Project Duration:** {round(total_profit):,} €")
st.write(f"**Effective Annual Return on Equity (EK):** {round(effective_annual_return)} %")
