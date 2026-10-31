import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Set page layout configuration
st.set_page_config(page_title="Astberg AF Fan Simulator", layout="wide")
st.title("📊 Astberg AF Series - Fan Selection Simulator")

# Core engineering catalog definitions
catalog = {
    'AF-100P': {'hs_max_cfm': 117, 'hs_max_sp': 15.9, 'ls_max_cfm': 97, 'ls_max_sp': 13.3, 'size': "4 inch (100mm)", 'db_hs': 31, 'db_ls': 24},
    'AF-125P': {'hs_max_cfm': 167, 'hs_max_sp': 16.2, 'ls_max_cfm': 146, 'ls_max_sp': 13.5, 'size': "5 inch (125mm)", 'db_hs': 32, 'db_ls': 26},
    'AF-150P': {'hs_max_cfm': 312, 'hs_max_sp': 30.6, 'ls_max_cfm': 241, 'ls_max_sp': 24.5, 'size': "6 inch (150mm)", 'db_hs': 33, 'db_ls': 27},
    'AF-200P': {'hs_max_cfm': 494, 'hs_max_sp': 35.9, 'ls_max_cfm': 406, 'ls_max_sp': 27.9, 'size': "8 inch (200mm)", 'db_hs': 38, 'db_ls': 32},
    'AF-250P': {'hs_max_cfm': 827, 'hs_max_sp': 51.4, 'ls_max_cfm': 624, 'ls_max_sp': 38.9, 'size': "10 inch (250mm)", 'db_hs': 50, 'db_ls': 44},
    'AF-315P': {'hs_max_cfm': 1298, 'hs_max_sp': 70.7, 'ls_max_cfm': 1030, 'ls_max_sp': 55.8, 'size': "12 inch (315mm)", 'db_hs': 53, 'db_ls': 47}
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
    db_level = specs['db_hs'] if speed == 'High Speed' else specs['db_ls']
st.info(f"**Noise Level:** {db_level} dB(A) at 3m")

import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Set page layout configuration
st.set_page_config(page_title="Multi-Brand Fan Simulator", layout="wide")
st.title("📊 Multi-Brand Fan Selection Simulator")
st.write("Cross-examine performance curves and find optimal models across both **Astberg AF** and **Kruger CCD** series.")

# Combined Engineering Catalog Matrix
# Note: Kruger data converted accurately from CMH/Pascals to standard operational CFM / mm of WC.
catalog = {
    # --- ASTBERG AF MIXED FLOW LINEUP ---
    'Astberg AF-100P': {'hs_max_cfm': 117, 'hs_max_sp': 15.9, 'ls_max_cfm': 97, 'ls_max_sp': 13.3, 'size': "4 inch (100mm)", 'db_hs': 31, 'db_ls': 24, 'brand': 'Astberg'},
    'Astberg AF-125P': {'hs_max_cfm': 167, 'hs_max_sp': 16.2, 'ls_max_cfm': 146, 'ls_max_sp': 13.5, 'size': "5 inch (125mm)", 'db_hs': 32, 'db_ls': 26, 'brand': 'Astberg'},
    'Astberg AF-150P': {'hs_max_cfm': 312, 'hs_max_sp': 30.6, 'ls_max_cfm': 241, 'ls_max_sp': 24.5, 'size': "6 inch (150mm)", 'db_hs': 33, 'db_ls': 27, 'brand': 'Astberg'},
    'Astberg AF-200P': {'hs_max_cfm': 494, 'hs_max_sp': 35.9, 'ls_max_cfm': 406, 'ls_max_sp': 27.9, 'size': "8 inch (200mm)", 'db_hs': 38, 'db_ls': 32, 'brand': 'Astberg'},
    'Astberg AF-250P': {'hs_max_cfm': 827, 'hs_max_sp': 51.4, 'ls_max_cfm': 624, 'ls_max_sp': 38.9, 'size': "10 inch (250mm)", 'db_hs': 50, 'db_ls': 44, 'brand': 'Astberg'},
    'Astberg AF-315P': {'hs_max_cfm': 1298, 'hs_max_sp': 70.7, 'ls_max_cfm': 1030, 'ls_max_sp': 55.8, 'size': "12 inch (315mm)", 'db_hs': 53, 'db_ls': 47, 'brand': 'Astberg'},
    
    # --- KRUGER CCD CABINET CENTRIFUGAL LINEUP ---
    'Kruger CCD 140': {'hs_max_cfm': 380, 'hs_max_sp': 28.0, 'ls_max_cfm': 290, 'ls_max_sp': 20.0, 'size': "Rectangular Flanged", 'db_hs': 51, 'db_ls': 44, 'brand': 'Kruger'},
    'Kruger CCD 160': {'hs_max_cfm': 530, 'hs_max_sp': 32.0, 'ls_max_cfm': 410, 'ls_max_sp': 22.0, 'size': "Rectangular Flanged", 'db_hs': 54, 'db_ls': 46, 'brand': 'Kruger'},
    'Kruger CCD 7-7':  {'hs_max_cfm': 940, 'hs_max_sp': 42.0, 'ls_max_cfm': 710, 'ls_max_sp': 30.0, 'size': "Rectangular Flanged", 'db_hs': 58, 'db_ls': 50, 'brand': 'Kruger'},
    'Kruger CCD 8-8':  {'hs_max_cfm': 1410, 'hs_max_sp': 48.0, 'ls_max_cfm': 1120, 'ls_max_sp': 34.0, 'size': "Rectangular Flanged", 'db_hs': 61, 'db_ls': 53, 'brand': 'Kruger'},
    'Kruger CCD 9-7':  {'hs_max_cfm': 1880, 'hs_max_sp': 55.0, 'ls_max_cfm': 1470, 'ls_max_sp': 38.0, 'size': "Rectangular Flanged", 'db_hs': 64, 'db_ls': 55, 'brand': 'Kruger'},
    'Kruger CCD 9-9':  {'hs_max_cfm': 2240, 'hs_max_sp': 58.0, 'ls_max_cfm': 1760, 'ls_max_sp': 41.0, 'size': "Rectangular Flanged", 'db_hs': 66, 'db_ls': 57, 'brand': 'Kruger'}
}

# Layout controls configuration
st.sidebar.header("⚙️ Brand Visibility Filters")
show_astberg = st.sidebar.checkbox("Show Astberg AF Series", value=True)
show_kruger = st.sidebar.checkbox("Show Kruger CCD Series", value=True)

col1, col2 = st.columns()

with col1:
    st.subheader("🎯 Enter Duty Design Points")
    input_cfm = st.number_input("Target Airflow Volume (CFM)", min_value=0.0, value=450.0, step=10.0)
    input_sp = st.number_input("Static Pressure (mm of WC)", min_value=0.0, value=20.0, step=1.0)
    
    # Run dynamic optimization search loop
    valid_options = []
    for model, specs in catalog.items():
        # Check brand visibility restrictions
        if specs['brand'] == 'Astberg' and not show_astberg:
            continue
        if specs['brand'] == 'Kruger' and not show_kruger:
            continue
            
        for speed in ['High Speed', 'Low Speed']:
            max_cfm = specs['hs_max_cfm'] if speed == 'High Speed' else specs['ls_max_cfm']
            max_sp = specs['hs_max_sp'] if speed == 'High Speed' else specs['ls_max_sp']
            
            if input_cfm <= max_cfm:
                # Target curve verification via quadratic pressure tracking
                available_sp = max_sp * (1 - (input_cfm / max_cfm)**2)
                if available_sp >= input_sp:
                    # Sort criteria optimized to favor stable 55% middle-curve selection paths
                    optimal_flow = max_cfm * 0.55
                    distance = abs(input_cfm - optimal_flow)
                    db_val = specs['db_hs'] if speed == 'High Speed' else specs['db_ls']
                    valid_options.append((distance, model, speed, available_sp, specs['size'], db_val, specs['brand']))
                    
    st.subheader("💡 Automated Recommendations Match")
    if valid_options:
        valid_options.sort() # Top index sorting isolates ideal operating margins
        best = valid_options[0]
        
        st.success(f"🥇 **Best Selection:** {best[1]}")
        st.info(f"**Manufacturer Brand:** {best[6]}\n\n"
                f"**Motor Step Value:** Runs on **{best[2]}**\n\n"
                f"**Physical Duct Orientation:** {best[4]}\n\n"
                f"**Acoustic Profile Index:** {best[5]} dB(A) at 3m\n\n"
                f"**Available Static Margin:** {best[3]:.2f} mm of WC (Target: {input_sp} mm)")
                
        if len(valid_options) > 1:
            with st.expander("🔄 View Alternative Matching Fan Models"):
                for opt in valid_options[1:4]:
                    st.write(f"• **{opt[1]}** ({opt[2]}) — Margin: {opt[3]:.1f} mm | Noise: {opt[5]} dB")
    else:
        st.error("❌ Selected duty point parameters fall outside current curve matrices. Try dividing flow loops or lowering target system static pressure values.")

with col2:
    fig = go.Figure()
    
    # Set unified distinct color tracks for all matching variations
    all_models = list(catalog.keys())
    color_map = {
        'Astberg AF-100P': '#1f77b4', 'Astberg AF-125P': '#ff7f0e', 'Astberg AF-150P': '#2ca02c',
        'Astberg AF-200P': '#d62728', 'Astberg AF-250P': '#9467bd', 'Astberg AF-315P': '#8c564b',
        'Kruger CCD 140': '#e377c2', 'Kruger CCD 160': '#7f7f7f', 'Kruger CCD 7-7': '#bcbd22',
        'Kruger CCD 8-8': '#17becf', 'Kruger CCD 9-7': '#1f77b4', 'Kruger CCD 9-9': '#9467bd'
    }
    
    for model, specs in catalog.items():
        if specs['brand'] == 'Astberg' and not show_astberg:
            continue
        if specs['brand'] == 'Kruger' and not show_kruger:
            continue
            
        color = color_map.get(model, '#000000')
        
        # Plot High Speed Track
        x_hs = np.linspace(0, specs['hs_max_cfm'], 50)
        y_hs = specs['hs_max_sp'] * (1 - (x_hs / specs['hs_max_cfm'])**2)
        fig.add_trace(go.Scatter(x=x_hs, y=y_hs, name=f"{model} (HS)", line=dict(color=color, width=2)))
        
        # Plot Low Speed Track
        x_ls = np.linspace(0, specs['ls_max_cfm'], 50)
        y_ls = specs['ls_max_sp'] * (1 - (x_ls / specs['ls_max_cfm'])**2)
        fig.add_trace(go.Scatter(x=x_ls, y=y_ls, name=f"{model} (LS)", line=dict(color=color, width=1.5, dash='dash')))

    # Overlay Target Coordinates Intersect Point
    fig.add_trace(go.Scatter(x=[input_cfm], y=[input_sp], name="Design Duty Coordinate",
                             marker=dict(color='black', size=14, symbol='x'), mode='markers'))

    fig.update_layout(
        title="Multi-Brand Performance Curve Graph Matrix", 
        xaxis_title="Airflow Volume (CFM)",
        yaxis_title="Static Pressure (mm of WC)", 
        xaxis=dict(range=[0, 2400]), 
        yaxis=dict(range=[0, 75]), 
        height=650
    )
    st.plotly_chart(fig, use_container_width=True)

