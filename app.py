import streamlit as st

# Sample protocol data
treatment_data = {
    "FOLFOX": {
        "drugs": [
            {"name": "5-FU", "dose_mg_per_m2": 400, "cost_per_mg": 0.30},
            {"name": "Oxaliplatin", "dose_mg_per_m2": 85, "cost_per_mg": 2.00}
        ],
        "delivery_cost_per_cycle": 800
    },
    "CHOP": {
        "drugs": [
            {"name": "Cyclophosphamide", "dose_mg_per_m2": 750, "cost_per_mg": 0.50},
            {"name": "Doxorubicin", "dose_mg_per_m2": 50, "cost_per_mg": 1.50},
        ],
        "delivery_cost_per_cycle": 700
    }
}

# BSA Calculation using Du Bois formula
def calculate_bsa(weight_kg, height_cm):
    return round(0.007184 * (weight_kg ** 0.425) * (height_cm ** 0.725), 2)

# Cost calculator
def calculate_total_cost(protocol, bsa, cycles):
    protocol_data = treatment_data[protocol]
    drug_cost = 0
    for drug in protocol_data["drugs"]:
        dose = drug["dose_mg_per_m2"] * bsa
        cost = dose * drug["cost_per_mg"]
        drug_cost += cost
    total_drug_cost = drug_cost * cycles
    delivery_cost = protocol_data["delivery_cost_per_cycle"] * cycles
    total_cost = total_drug_cost + delivery_cost
    return total_cost, total_drug_cost, delivery_cost

# UI
st.title("Oncology Treatment Cost Estimator")

protocol = st.selectbox("Select Treatment Protocol", list(treatment_data.keys()))
weight = st.number_input("Patient Weight (kg)", min_value=30.0, max_value=200.0, step=1.0)
height = st.number_input("Patient Height (cm)", min_value=100.0, max_value=250.0, step=1.0)
cycles = st.number_input("Number of Treatment Cycles", min_value=1, max_value=20, step=1)

if st.button("Estimate Cost"):
    bsa = calculate_bsa(weight, height)
    total, drug, delivery = calculate_total_cost(protocol, bsa, cycles)

    st.subheader("Estimate Summary")
    st.write(f"Body Surface Area (BSA): **{bsa} m²**")
    st.write(f"Total Drug Cost: **${drug:,.2f}**")
    st.write(f"Total Delivery Cost: **${delivery:,.2f}**")
    st.success(f"**Estimated Total Cost: ${total:,.2f}**")