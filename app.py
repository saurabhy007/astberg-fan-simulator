import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Set page layout configuration
st.set_page_config(page_title="Astberg AF Fan Simulator", layout="wide")
st.title("📊 Astberg AF Series - Fan Selection Simulator")

# Core engineering catalog definitions
catalog = {
    'AF-100P': {'hs_max_cfm': 117, 'hs_max_sp': 15.9, 'ls_max_cfm': 97, 'ls_max_sp': 13.3, 'size': "4 inch (100mm)"},
    'AF-125P': {'hs_max_cfm': 167, 'hs_max_sp': 16.2, 'ls_max_cfm': 146, 'ls_max_sp': 13.5, 'size': "5 inch (125mm)"},
    'AF-150P': {'hs_max_cfm': 312, 'hs_max_sp': 30.6, 'ls_max_cfm': 241, 'ls_max_sp': 24.5, 'size': "6 inch (150mm)"},
    'AF-200P': {'hs_max_cfm': 494, 'hs_max_sp': 35.9, 'ls_max_cfm': 406, 'ls_max_sp': 27.9, 'size': "8 inch (200mm)"},
    'AF-250P': {'hs_max_cfm': 827, 'hs_max_sp': 51.4, 'ls_max_cfm': 624, 'ls_max_sp': 38.9, 'size': "10 inch (250mm)"},
    'AF-315P': {'hs_max_cfm': 1298, 'hs_max_sp': 70.7, 'ls_max_cfm': 1030, 'ls_max_sp': 55.8, 'size': "12 inch (315mm)"}
}

# Interface Split Layout
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🎯 Enter Duty Design Points")
    input_cfm = st.number_input("Target Airflow (CFM)", min_value=0.0, value=100.0, step=10.0)
    input_sp = st.number_input("Static Pressure (mm of WC)", min_value=0.0, value=15.0, step=1.0)
    
    # Selection Optimization Engine
    valid_options = []
    for model, specs in catalog.items():
        for speed in ['High Speed', 'Low Speed']:
            max_cfm = specs['hs_max_cfm'] if speed == 'High Speed' else specs['ls_max_cfm']
            max_sp = specs['hs_max_sp'] if speed == 'High Speed' else specs['ls_max_sp']
            
            if input_cfm <= max_cfm:
                available_sp = max_sp * (1 - (input_cfm / max_cfm)**2)
                if available_sp >= input_sp:
                    # Calculate proximity to optimal middle operational zone (approx 55% flow)
                    optimal_flow = max_cfm * 0.55
                    distance = abs(input_cfm - optimal_flow)
                    valid_options.append((distance, model, speed, available_sp, specs['size']))
                    
    st.subheader("💡 Automated Recommendation")
    if valid_options:
        valid_options.sort() # Top match handles efficiency optimization
        best_match = valid_options[0]
        st.success(f"**Recommended Model:** {best_match[1]}")
        st.info(f"**Operational Velocity:** Runs on **{best_match[2]}**\n\n"
                f"**Collar Duct Connection:** {best_match[4]}\n\n"
                f"**Available Static Margin:** {best_match[3]:.2f} mm of WC (Target: {input_sp} mm)")
    else:
        st.error("❌ Duty point exceeds all available model specifications. Try lower static limits or break down into multiple branches.")

with col2:
    fig = go.Figure()
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
    
    for idx, (model, specs) in enumerate(catalog.items()):
        # High Speed Plot Line
        x_hs = np.linspace(0, specs['hs_max_cfm'], 50)
        y_hs = specs['hs_max_sp'] * (1 - (x_hs / specs['hs_max_cfm'])**2)
        fig.add_trace(go.Scatter(x=x_hs, y=y_hs, name=f"{model} (HS)", line=dict(color=colors[idx], width=2)))
        
        # Low Speed Plot Line
        x_ls = np.linspace(0, specs['ls_max_cfm'], 50)
        y_ls = specs['ls_max_sp'] * (1 - (x_ls / specs['ls_max_cfm'])**2)
        fig.add_trace(go.Scatter(x=x_ls, y=y_ls, name=f"{model} (LS)", line=dict(color=colors[idx], width=1.5, dash='dash')))

    # Add Target Design Point Intersection Dot
    fig.add_trace(go.Scatter(x=[input_cfm], y=[input_sp], name="Your Design Point",
                             marker=dict(color='black', size=12, symbol='cross'), mode='markers'))

    fig.update_layout(
    title="System Performance Curve Graph Matrix", 
    xaxis_title="Airflow Volume (CFM)",
    yaxis_title="Static Pressure (mm of WC)", 
    xaxis=dict(range=[0, 1400]), 
    yaxis=dict(range=[0, 75]), 
    height=600
)
    st.plotly_chart(fig, use_container_width=True)
