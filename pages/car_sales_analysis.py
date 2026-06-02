"""
Car Sales Analysis Dashboard - Streamlit Page
Year-on-Year growth, forecasting, and deviation analysis for Indian car sales
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os
from pathlib import Path

from src.car_sales_analyzer import CarSalesAnalyzer

# Page configuration
st.set_page_config(
    page_title="Car Sales Analysis",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .metric-card {
        background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%);
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #667eea;
        margin: 10px 0;
    }
    
    .fuel-type-section {
        background: white;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        margin: 15px 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }
    
    .deviation-flag {
        background: linear-gradient(135deg, #ffebee 0%, #ffe0e6 100%);
        padding: 15px;
        border-left: 5px solid #f44336;
        border-radius: 8px;
        margin: 10px 0;
    }
    
    .growth-positive {
        color: #4caf50;
        font-weight: bold;
    }
    
    .growth-negative {
        color: #f44336;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)


def load_and_analyze_data():
    """Load CSV data and perform analysis"""
    csv_path = "data/car_sales_india.csv"
    
    if not os.path.exists(csv_path):
        st.error(f"❌ Data file not found: {csv_path}")
        return None
    
    try:
        analyzer = CarSalesAnalyzer(csv_path)
        return analyzer
    except Exception as e:
        st.error(f"❌ Error loading data: {str(e)}")
        return None


def display_header():
    """Display page header"""
    col1, col2 = st.columns([4, 1])
    
    with col1:
        st.markdown("""
        <div style="padding: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; color: white;">
            <h1 style="margin: 0; font-size: 2.2em;">🚗 Indian Car Sales Analysis</h1>
            <p style="margin: 10px 0 0 0; font-size: 1.05em;">Year-on-Year Growth, Forecasting & Deviation Analysis</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.info("📊 Real-time analysis of Petrol, Diesel, EV & Hybrid sales")


def display_summary_stats(stats):
    """Display summary statistics for each fuel type"""
    st.markdown("## 📈 Summary Statistics")
    
    cols = st.columns(4)
    fuel_types = ["Petrol", "Diesel", "EV", "Hybrid"]
    colors = ["#FF9800", "#8B4513", "#00C853", "#00BCD4"]
    
    for col, fuel, color in zip(cols, fuel_types, colors):
        with col:
            data = stats[fuel]
            st.markdown(f"""
            <div class="metric-card" style="border-left-color: {color};">
                <h3 style="margin: 0 0 15px 0; color: {color};">{fuel}</h3>
                <p><strong>Current (2026):</strong> {data['current_sales']:,} units</p>
                <p><strong>Avg YoY:</strong> <span class="growth-positive">{data['avg_yoy']:+.2f}%</span></p>
                <p><strong>Total Growth:</strong> <span class="growth-positive">{data['total_growth']:+.2f}%</span></p>
                <p style="margin: 0; color: #666; font-size: 0.9em;">Range: {data['min_yoy']:.2f}% to {data['max_yoy']:.2f}%</p>
            </div>
            """, unsafe_allow_html=True)


def display_yoy_table(yoy_data):
    """Display YoY growth table"""
    st.markdown("## 📊 Year-on-Year Growth (%)")
    
    # Format the data for display
    display_df = yoy_data.copy()
    for col in ["Petrol_YoY", "Diesel_YoY", "EV_YoY", "Hybrid_YoY"]:
        if col in display_df.columns:
            display_df[col] = display_df[col].apply(lambda x: f"{x:+.2f}%" if pd.notna(x) else "—")
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)


def display_yoy_chart(analyzer):
    """Display interactive YoY growth chart"""
    st.markdown("## 📉 YoY Growth Trends")
    
    fig = go.Figure()
    
    for fuel_type, color in [("Petrol", "#FF9800"), ("Diesel", "#8B4513"), 
                              ("EV", "#00C853"), ("Hybrid", "#00BCD4")]:
        fig.add_trace(go.Scatter(
            x=analyzer.data["Year"],
            y=analyzer.data[f"{fuel_type}_YoY"],
            mode='lines+markers',
            name=fuel_type,
            line=dict(color=color, width=3),
            marker=dict(size=8),
            hovertemplate=f"<b>{fuel_type}</b><br>Year: %{{x}}<br>YoY: %{{y:.2f}}%<extra></extra>"
        ))
    
    fig.add_hline(
        y=30, line_dash="dash", line_color="red", 
        annotation_text="<b>Critical</b> (30%)", annotation_position="right"
    )
    fig.add_hline(
        y=-30, line_dash="dash", line_color="red"
    )
    
    fig.update_layout(
        title="<b>Year-on-Year Growth Comparison</b>",
        xaxis_title="Year",
        yaxis_title="Growth (%)",
        height=450,
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Arial, sans-serif", size=12)
    )
    
    st.plotly_chart(fig, use_container_width=True)


def display_deviation_analysis(analyzer):
    """Display deviation flagged years"""
    st.markdown("## 🚨 Deviation Analysis (>30%)")
    
    deviations = analyzer.deviations
    
    has_deviations = False
    for fuel, flagged_years in deviations.items():
        if flagged_years:
            has_deviations = True
            st.markdown(f"### {fuel}")
            
            for record in flagged_years:
                year = int(record['Year']) if 'Year' in record else record.get('Year', 'N/A')
                yoy = record.get(f'{fuel}_YoY', 0)
                
                severity = "🔴 CRITICAL" if abs(yoy) > 30 else "🟡 WARNING"
                
                st.markdown(f"""
                <div class="deviation-flag">
                    <strong>{severity} - Year {year}:</strong> YoY = <span class="growth-positive">{yoy:+.2f}%</span>
                </div>
                """, unsafe_allow_html=True)
    
    if not has_deviations:
        st.success("✅ No critical deviations detected (>30%)")


def display_forecasts(analyzer):
    """Display forecasts with interactive chart"""
    st.markdown("## 🔮 Sales Forecast (Next 3 Years)")
    
    # Get historical data
    historical_data = {
        'Year': analyzer.data['Year'].tolist(),
        'Petrol': analyzer.data['Petrol'].tolist(),
        'Diesel': analyzer.data['Diesel'].tolist(),
        'EV': analyzer.data['EV'].tolist(),
        'Hybrid': analyzer.data['Hybrid'].tolist()
    }
    
    fig = go.Figure()
    
    colors = {"Petrol": "#FF9800", "Diesel": "#8B4513", "EV": "#00C853", "Hybrid": "#00BCD4"}
    
    # Add historical data
    for fuel_type, color in colors.items():
        fig.add_trace(go.Scatter(
            x=historical_data['Year'],
            y=historical_data[fuel_type],
            mode='lines+markers',
            name=f"{fuel_type} (Historical)",
            line=dict(color=color, width=3),
            marker=dict(size=8),
            hovertemplate=f"<b>{fuel_type}</b><br>Year: %{{x}}<br>Sales: %{{y:,}}<extra></extra>"
        ))
    
    # Add forecasts
    for fuel_type, color in colors.items():
        forecast = analyzer.forecast_trend(fuel_type, years_ahead=3)
        
        fig.add_trace(go.Scatter(
            x=forecast['years'],
            y=forecast['values'],
            mode='lines+markers',
            name=f"{fuel_type} (Forecast)",
            line=dict(color=color, width=2, dash='dash'),
            marker=dict(size=8, symbol='diamond'),
            hovertemplate=f"<b>{fuel_type} Forecast</b><br>Year: %{{x}}<br>Forecast: %{{y:,.0f}}<extra></extra>"
        ))
    
    fig.update_layout(
        title="<b>Sales Forecast (2027-2029)</b>",
        xaxis_title="Year",
        yaxis_title="Units Sold",
        height=500,
        hovermode='x unified',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Arial, sans-serif", size=12)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display forecast details
    st.markdown("### Forecast Details")
    
    for fuel_type in ["Petrol", "Diesel", "EV", "Hybrid"]:
        forecast = analyzer.forecasts[fuel_type]
        slope = forecast['slope']
        trend = "📈 Increasing" if slope > 0 else "📉 Decreasing"
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                fuel_type,
                f"{int(forecast['values'][-1]):,}",
                f"{slope:,.0f} units/year",
                help=f"2029 forecast: {int(forecast['values'][-1]):,} units"
            )


def display_sales_comparison():
    """Display sales units comparison chart"""
    st.markdown("## 📊 Sales Volume Comparison")
    
    analyzer = load_and_analyze_data()
    if not analyzer:
        return
    
    # Get data for last 5 years
    recent_data = analyzer.data[analyzer.data['Year'] >= 2021].copy()
    
    fig = go.Figure()
    
    for fuel_type, color in [("Petrol", "#FF9800"), ("Diesel", "#8B4513"), 
                              ("EV", "#00C853"), ("Hybrid", "#00BCD4")]:
        fig.add_trace(go.Bar(
            x=recent_data['Year'],
            y=recent_data[fuel_type],
            name=fuel_type,
            marker_color=color,
            hovertemplate=f"<b>{fuel_type}</b><br>Year: %{{x}}<br>Sales: %{{y:,}} units<extra></extra>"
        ))
    
    fig.update_layout(
        title="<b>Sales Volume by Fuel Type (2021-2026)</b>",
        xaxis_title="Year",
        yaxis_title="Units Sold",
        barmode='group',
        height=400,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family="Arial, sans-serif", size=12)
    )
    
    st.plotly_chart(fig, use_container_width=True)


def display_market_share():
    """Display market share evolution"""
    st.markdown("## 🥧 Market Share Evolution")
    
    analyzer = load_and_analyze_data()
    if not analyzer:
        return
    
    # Calculate market share for selected years
    years_to_show = [2015, 2018, 2022, 2026]
    
    cols = st.columns(len(years_to_show))
    
    for col, year in zip(cols, years_to_show):
        year_data = analyzer.data[analyzer.data['Year'] == year]
        
        if not year_data.empty:
            petrol = year_data['Petrol'].values[0]
            diesel = year_data['Diesel'].values[0]
            ev = year_data['EV'].values[0]
            hybrid = year_data['Hybrid'].values[0]
            
            with col:
                fig = go.Figure(data=[
                    go.Pie(
                        labels=['Petrol', 'Diesel', 'EV', 'Hybrid'],
                        values=[petrol, diesel, ev, hybrid],
                        marker=dict(colors=['#FF9800', '#8B4513', '#00C853', '#00BCD4']),
                        textposition='inside',
                        textinfo='label+percent'
                    )
                ])
                
                fig.update_layout(
                    title=f"<b>{year}</b>",
                    height=350,
                    font=dict(size=10)
                )
                
                st.plotly_chart(fig, use_container_width=True)


def main():
    """Main dashboard"""
    display_header()
    st.divider()
    
    # Load analyzer
    analyzer = load_and_analyze_data()
    if not analyzer:
        return
    
    # Perform analysis
    analyzer.calculate_yoy_growth()
    analyzer.detect_deviations()
    stats = analyzer.get_summary_stats()
    
    # Display sections
    display_summary_stats(stats)
    st.divider()
    
    display_sales_comparison()
    st.divider()
    
    display_yoy_chart(analyzer)
    st.divider()
    
    display_yoy_table(analyzer.calculate_yoy_growth())
    st.divider()
    
    display_deviation_analysis(analyzer)
    st.divider()
    
    display_forecasts(analyzer)
    st.divider()
    
    display_market_share()
    st.divider()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    ### 📌 Analysis Notes
    - **Deviation Threshold:** 30% (Critical), 15% (Warning)
    - **Forecast Method:** Linear regression trend analysis
    - **Data Currency:** Sales figures in units (actual vehicle count)
    - **Last Updated:** 2026-06-02
    """)


if __name__ == "__main__":
    main()
