"""
ProjectTracker - Real Estate Variance Analysis Dashboard
Main Streamlit Application with Enhanced UI
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import io

from src.database import (
    get_all_projects, get_project_parameters, add_project, 
    add_parameter, update_actual_value
)
from src.variance_engine import VarianceAnalyzer
from src.utils import parse_csv, validate_project_data, format_currency, format_percentage

# ==================== Helper Functions ====================

def format_for_display(value, currency="₹"):
    """Format numeric value for display with Indian Rupees"""
    if pd.isna(value):
        return "—"
    if isinstance(value, (int, float)):
        return f"{currency} {value:,.2f}"
    return str(value)

# Page configuration
st.set_page_config(
    page_title="ProjectTracker - Variance Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced Custom CSS with Professional Styling
st.markdown("""
    <style>
    /* Main theme colors */
    :root {
        --primary: #667eea;
        --secondary: #764ba2;
        --success: #4caf50;
        --warning: #ff9800;
        --danger: #f44336;
        --info: #2196F3;
    }
    
    /* Metric cards with gradient */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 25px;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    
    /* Status badges */
    .status-ok {
        background-color: #e8f5e9;
        color: #2e7d32;
        padding: 6px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85em;
        display: inline-block;
    }
    
    .status-warning {
        background-color: #fff3e0;
        color: #e65100;
        padding: 6px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85em;
        display: inline-block;
    }
    
    .status-critical {
        background-color: #ffebee;
        color: #c62828;
        padding: 6px 12px;
        border-radius: 20px;
        font-weight: 600;
        font-size: 0.85em;
        display: inline-block;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    /* Deviation alert box */
    .deviation-flag {
        background: linear-gradient(135deg, #ffebee 0%, #ffe0e6 100%);
        padding: 18px;
        border-left: 5px solid #f44336;
        border-radius: 8px;
        margin: 15px 0;
        box-shadow: 0 2px 8px rgba(244, 67, 54, 0.15);
    }
    
    /* Parameter card */
    .param-card {
        background: white;
        border: 1px solid #e0e0e0;
        padding: 16px;
        border-radius: 8px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    .param-card:hover {
        border-color: #667eea;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
    }
    
    /* Header styling */
    .header-title {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.5em;
        font-weight: 700;
        margin-bottom: 10px;
    }
    
    .header-subtitle {
        color: #666;
        font-size: 1.1em;
        font-weight: 500;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f5f5f5;
        border-radius: 8px 8px 0 0;
        padding: 12px 20px;
        font-weight: 600;
    }
    
    /* Divider */
    .stDivider {
        margin: 20px 0;
        border: 1px solid #e0e0e0;
    }
    
    /* Info/Warning boxes */
    .stInfo, .stWarning, .stError, .stSuccess {
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if "refresh" not in st.session_state:
    st.session_state.refresh = False

def initialize_app():
    """Initialize app state"""
    if "current_project_id" not in st.session_state:
        st.session_state.current_project_id = None
    if "analyzer" not in st.session_state:
        st.session_state.analyzer = VarianceAnalyzer()


def render_status_badge(deviation):
    """Render a status badge based on deviation percentage"""
    if deviation is None or pd.isna(deviation):
        return '<span class="status-warning">⏳ PENDING</span>'
    abs_dev = abs(deviation)
    if abs_dev > 30:
        return f'<span class="status-critical">🚨 CRITICAL ({abs_dev:.1f}%)</span>'
    elif abs_dev > 15:
        return f'<span class="status-warning">⚠️ WARNING ({abs_dev:.1f}%)</span>'
    else:
        return f'<span class="status-ok">✅ OK ({abs_dev:.1f}%)</span>'


def create_summary_metrics(summary):
    """Create summary metrics display with enhanced styling"""
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "📊 Total Parameters",
            summary["total_parameters"],
            help="Total number of parameters tracked"
        )
    
    with col2:
        st.metric(
            "🚨 Critical Deviations",
            summary["flagged_count"],
            delta=f"{(summary['flagged_count']/max(summary['total_parameters'], 1)*100):.1f}%",
            help="Deviations exceeding 30% threshold"
        )
    
    with col3:
        st.metric(
            "✅ Within Limits",
            summary["ok_count"],
            help="Parameters within acceptable range"
        )
    
    with col4:
        st.metric(
            "⏳ Pending",
            summary.get("pending_count", 0),
            help="Parameters without actual values"
        )
    
    with col5:
        st.metric(
            "📈 Avg Deviation",
            f"{summary['avg_deviation']:.2f}%",
            help="Average absolute deviation percentage"
        )


def create_project_header(project_name, project_desc, project_date):
    """Create an enhanced project header"""
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        st.markdown(f"""
        <div style="padding: 20px; background: linear-gradient(135deg, #667eea15 0%, #764ba215 100%); border-radius: 12px; border-left: 5px solid #667eea;">
            <h2 style="margin: 0; color: #333;">{project_name}</h2>
            <p style="margin: 8px 0 0 0; color: #666; font-size: 0.95em;">{project_desc if project_desc else "Real Estate Project"}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.caption(f"📅 Start Date")
        st.write(project_date)
    
    with col3:
        st.caption(f"🔄 Last Updated")
        st.write(datetime.now().strftime("%Y-%m-%d"))


def main():
    """Main application with enhanced UI"""
    initialize_app()
    
    # Header with enhanced styling
    col1, col2 = st.columns([4, 1])
    with col1:
        st.markdown('<div class="header-title">📊 ProjectTracker</div>', unsafe_allow_html=True)
        st.markdown('<div class="header-subtitle">Real Estate Variance Analysis & Monitoring System</div>', unsafe_allow_html=True)
    
    with col2:
        # Theme toggle and settings
        with st.popover("⚙️ Settings"):
            st.markdown("**Theme Settings**")
            theme = st.radio("Select theme", ["Light", "Dark"], horizontal=True)
            st.divider()
            st.markdown("**About**")
            st.caption("ProjectTracker v1.0 | Monitor projected vs actual parameters")
    
    st.divider()
    
    # Sidebar with enhanced styling
    with st.sidebar:
        st.markdown("## 🚀 Navigation")
        
        # Project selection
        projects = get_all_projects()
        project_names = [p[1] for p in projects] if projects else []
        
        selected_project = st.selectbox(
            "Select Project",
            options=project_names if project_names else ["No projects"],
            key="project_selector"
        )
        
        # Get selected project ID
        if selected_project and selected_project != "No projects" and projects:
            st.session_state.current_project_id = next(
                (p[0] for p in projects if p[1] == selected_project), None
            )
        
        st.divider()
        
        # Create new project section
        st.markdown("### ➕ Create New Project")
        
        with st.form("new_project_form"):
            new_project_name = st.text_input(
                "Project Name",
                placeholder="e.g., Mumbai Tower Complex",
                help="Unique project identifier"
            )
            new_project_desc = st.text_area(
                "Description",
                placeholder="Project details, location, etc.",
                height=80,
                help="Optional project description"
            )
            new_project_date = st.date_input(
                "Start Date",
                value=datetime.now(),
                help="Project start date"
            )
            
            submitted = st.form_submit_button(
                "✨ Create Project",
                use_container_width=True
            )
            
            if submitted:
                if new_project_name.strip():
                    project_id = add_project(
                        new_project_name,
                        new_project_desc,
                        str(new_project_date)
                    )
                    if project_id:
                        st.success(f"✅ Project '{new_project_name}' created successfully!")
                        st.session_state.refresh = True
                        st.rerun()
                    else:
                        st.error("❌ Project name already exists!")
                else:
                    st.warning("⚠️ Please enter a project name")
        
        st.divider()
        st.caption("💡 Tip: Select a project to start tracking variance")
    
    # Main content area
    if not st.session_state.current_project_id:
        # Welcome screen
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div style="text-align: center; padding: 60px 20px;">
                <h2 style="color: #667eea;">👈 Get Started</h2>
                <p style="font-size: 1.1em; color: #666;">Select an existing project or create a new one from the sidebar</p>
                
                <div style="margin-top: 40px; padding: 20px; background: #f5f5f5; border-radius: 12px;">
                    <h3 style="color: #333; margin-top: 0;">Quick Start Guide</h3>
                    <ol style="text-align: left; color: #666; line-height: 1.8;">
                        <li>Create a new project using the sidebar</li>
                        <li>Add parameters (budget, timeline, etc.)</li>
                        <li>Input actual values as work progresses</li>
                        <li>Monitor deviations in the dashboard</li>
                    </ol>
                </div>
            </div>
            """, unsafe_allow_html=True)
        return
    
    # Get current project details
    projects = get_all_projects()
    current_project = next(
        (p for p in projects if p[0] == st.session_state.current_project_id), None
    )
    
    if not current_project:
        st.error("❌ Project not found")
        return
    
    project_id, project_name, project_desc, project_date = current_project
    
    # Project header
    create_project_header(project_name, project_desc, project_date)
    
    st.divider()
    
    # Tabs with icons
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📈 Dashboard",
        "➕ Add Parameters",
        "📥 Import CSV",
        "🔍 Analysis",
        "📞 Help"
    ])
    
    # ==================== TAB 1: Dashboard ====================
    with tab1:
        st.markdown("## 📊 Variance Dashboard")
        
        params = get_project_parameters(project_id)
        
        if not params:
            st.info("📋 No parameters added yet. Go to the 'Add Parameters' tab to get started.")
        else:
            # Analyze variance
            analyzer = st.session_state.analyzer
            df_analysis = analyzer.analyze_project([
                (p[1], p[2], p[3], p[4], p[0]) for p in params
            ])
            
            if not df_analysis.empty:
                # Summary metrics
                summary = analyzer.generate_summary(df_analysis)
                create_summary_metrics(summary)
                
                st.divider()
                
                # Variance table with enhanced styling
                st.markdown("### 📋 Parameter Analysis Table")
                
                display_df = df_analysis.copy()
                display_df['Status'] = display_df['% Deviation'].apply(
                    lambda x: render_status_badge(x),
                    convert_dtype=False
                )
                
                # Format currency columns for display
                display_df['Projected'] = display_df['Projected'].apply(lambda x: format_for_display(x))
                display_df['Actual'] = display_df['Actual'].apply(lambda x: format_for_display(x))
                display_df['Variance'] = display_df['Variance'].apply(lambda x: format_for_display(x))
                
                # Create displayable dataframe
                display_cols = ['Parameter', 'Projected', 'Actual', 'Unit', 'Variance', '% Deviation', 'Status']
                display_df = display_df[display_cols]
                
                st.dataframe(
                    display_df,
                    use_container_width=True,
                    hide_index=True,
                    height=300
                )
                
                # Flagged deviations alert
                flagged_df = analyzer.get_flagged_parameters(df_analysis)
                if not flagged_df.empty:
                    st.divider()
                    with st.container(border=True):
                        st.markdown(f"### 🚨 Critical Deviations ({len(flagged_df)})")
                        
                        for idx, row in flagged_df.iterrows():
                            dev_color = "#f44336" if abs(row['% Deviation']) > 30 else "#ff9800"
                            proj_display = format_for_display(row['Projected'])
                            actual_display = format_for_display(row['Actual'])
                            var_display = format_for_display(row['Variance'])
                            st.markdown(f"""
                            <div class="param-card" style="border-left: 4px solid {dev_color};">
                                <div style="display: flex; justify-content: space-between; align-items: center;">
                                    <div>
                                        <strong style="font-size: 1.1em; color: #333;">{row['Parameter']}</strong>
                                        <p style="margin: 5px 0; color: #666; font-size: 0.9em;">
                                            Projected: <strong>{proj_display} {row['Unit']}</strong> → 
                                            Actual: <strong>{actual_display} {row['Unit']}</strong>
                                        </p>
                                    </div>
                                    <div style="text-align: right;">
                                        <div style="font-size: 1.5em; font-weight: 700; color: {dev_color};">
                                            {row['% Deviation']:.1f}%
                                        </div>
                                        <div style="font-size: 0.85em; color: #999;">
                                            Variance: {var_display}
                                        </div>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                
                # Visualizations
                st.divider()
                st.markdown("### 📉 Visualizations")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Projected vs Actual comparison
                    fig_comp = go.Figure()
                    
                    fig_comp.add_trace(go.Bar(
                        name='Projected',
                        x=df_analysis['Parameter'],
                        y=df_analysis['Projected'],
                        marker_color='rgba(102, 126, 234, 0.7)',
                        marker_line_color='#667eea',
                        marker_line_width=1.5
                    ))
                    
                    fig_comp.add_trace(go.Bar(
                        name='Actual',
                        x=df_analysis['Parameter'],
                        y=df_analysis['Actual'],
                        marker_color='rgba(118, 75, 162, 0.7)',
                        marker_line_color='#764ba2',
                        marker_line_width=1.5
                    ))
                    
                    fig_comp.update_layout(
                        title="<b>Projected vs Actual Comparison</b>",
                        barmode='group',
                        height=450,
                        hovermode='x unified',
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(family="Arial, sans-serif", size=12),
                        title_font=dict(size=16, color="#333")
                    )
                    
                    st.plotly_chart(fig_comp, use_container_width=True)
                
                with col2:
                    # Deviation chart
                    colors = ['#f44336' if abs(x) > 30 else '#ff9800' if abs(x) > 15 else '#4caf50' for x in df_analysis['% Deviation']]
                    
                    fig_dev = go.Figure(data=[
                        go.Bar(
                            x=df_analysis['Parameter'],
                            y=df_analysis['% Deviation'],
                            marker_color=colors,
                            marker_line_color='darkred',
                            marker_line_width=1.5,
                            name='Deviation %'
                        )
                    ])
                    
                    fig_dev.add_hline(
                        y=30,
                        line_dash="dash",
                        line_color="#f44336",
                        annotation_text="<b>Critical</b> (30%)",
                        annotation_position="right"
                    )
                    
                    fig_dev.add_hline(
                        y=-30,
                        line_dash="dash",
                        line_color="#f44336"
                    )
                    
                    fig_dev.add_hline(
                        y=15,
                        line_dash="dot",
                        line_color="#ff9800",
                        annotation_text="<b>Warning</b> (15%)",
                        annotation_position="right"
                    )
                    
                    fig_dev.add_hline(
                        y=-15,
                        line_dash="dot",
                        line_color="#ff9800"
                    )
                    
                    fig_dev.update_layout(
                        title="<b>Deviation from Projection</b>",
                        yaxis_title="Deviation %",
                        height=450,
                        hovermode='x',
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(family="Arial, sans-serif", size=12),
                        title_font=dict(size=16, color="#333")
                    )
                    
                    st.plotly_chart(fig_dev, use_container_width=True)
                
                # Export options
                st.divider()
                st.markdown("### 💾 Export Results")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    csv = df_analysis.to_csv(index=False)
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv,
                        file_name=f"{project_name}_variance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv",
                        use_container_width=True
                    )
                
                with col2:
                    excel_buffer = io.BytesIO()
                    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                        df_analysis.to_excel(writer, index=False, sheet_name='Variance Analysis')
                    excel_buffer.seek(0)
                    st.download_button(
                        label="📊 Download Excel",
                        data=excel_buffer,
                        file_name=f"{project_name}_variance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                
                with col3:
                    # PDF export (optional)
                    st.button(
                        "📄 Generate Report",
                        use_container_width=True,
                        help="Generate PDF report (coming soon)"
                    )
    
    # ==================== TAB 2: Add Parameters ====================
    with tab2:
        st.markdown("## ➕ Add Project Parameters")
        st.caption("Add individual parameters to track project variance")
        
        st.warning("💰 **Currency Note:** All financial values must be entered in **Indian Rupees (₹)**. Examples: ₹ Crore (10 Million), ₹ Lakh (100,000), or ₹ (Rupees). DO NOT use USD or any other currency.")
        
        with st.form("add_parameter_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                param_name = st.text_input(
                    "Parameter Name",
                    placeholder="e.g., Budget, Completion Time, Units Sold",
                    help="Name of the parameter to track"
                )
                param_projected = st.number_input(
                    "Projected Value",
                    value=0.0,
                    step=0.01,
                    help="Expected or budgeted value"
                )
            
            with col2:
                param_unit = st.text_input(
                    "Unit of Measurement",
                    placeholder="e.g., ₹ Crore (INR), months, units, %",
                    max_chars=30,
                    help="Use ₹ for Indian Rupees. Examples: ₹ Crore, ₹ Lakh, ₹ (for rupees)"
                )
                param_actual = st.number_input(
                    "Actual Value (Optional)",
                    value=0.0,
                    step=0.01,
                    help="Current/actual value (can be updated later)"
                )
            
            submitted = st.form_submit_button(
                "✨ Add Parameter",
                use_container_width=True
            )
            
            if submitted:
                if param_name.strip() and param_projected > 0:
                    param_id = add_parameter(project_id, param_name, param_projected, param_unit)
                    if param_actual > 0:
                        update_actual_value(param_id, param_actual)
                    st.success(f"✅ Parameter '{param_name}' added successfully!")
                    st.rerun()
                else:
                    st.error("❌ Please enter valid parameter name and projected value (> 0)")
        
        st.divider()
        
        # Show existing parameters
        st.markdown("### 📋 Current Parameters")
        params = get_project_parameters(project_id)
        
        if params:
            analyzer = st.session_state.analyzer
            df_params = pd.DataFrame(
                params,
                columns=['ID', 'Name', 'Projected', 'Actual', 'Unit']
            )
            
            # Calculate deviation for each parameter
            deviations = []
            for _, row in df_params.iterrows():
                if row['Actual'] is not None and row['Actual'] > 0 and row['Projected'] > 0:
                    var = row['Actual'] - row['Projected']
                    pct_dev = (var / row['Projected']) * 100
                    deviations.append(pct_dev)
                else:
                    deviations.append(None)
            
            df_params['Deviation %'] = deviations
            
            for idx, param in enumerate(params):
                param_id, param_name, projected, actual, unit = param
                
                col1, col2, col3, col4 = st.columns([2, 1.5, 1.5, 1])
                
                with col1:
                    st.markdown(f"**{param_name}** ({unit})")
                
                with col2:
                    st.metric(
                        "Projected",
                        format_for_display(projected),
                        help="Projected value"
                    )
                
                with col3:
                    if actual is not None:
                        if projected > 0:
                            deviation = ((actual - projected) / projected) * 100
                            st.metric(
                                "Actual",
                                format_for_display(actual),
                                delta=f"{deviation:.1f}%",
                                help="Actual value with deviation"
                            )
                        else:
                            st.metric("Actual", format_for_display(actual), help="Actual value")
                    else:
                        st.metric("Actual", "—", help="Not set yet")
                
                with col4:
                    if st.button("✏️ Update", key=f"update_{param_id}", use_container_width=True):
                        with st.form(f"update_form_{param_id}"):
                            new_actual = st.number_input(
                                "New Actual Value",
                                value=float(actual) if actual is not None else 0.0,
                                step=0.01
                            )
                            if st.form_submit_button("Save", use_container_width=True):
                                update_actual_value(param_id, new_actual)
                                st.success(f"✅ Updated!")
                                st.rerun()
                
                st.divider()
        else:
            st.info("📭 No parameters yet. Add one above!")
    
    # ==================== TAB 3: Import CSV ====================
    with tab3:
        st.markdown("## 📥 Import Data from CSV")
        
        st.warning("🇮🇳 **Currency Requirement:** All financial values in your CSV must be in **Indian Rupees (₹)**. Use units like ₹ Crore, ₹ Lakh, or ₹. DO NOT import USD or any other currency.")
        
        st.info(
            "📋 **Required columns:** Parameter, Projected  \n"
            "**Optional columns:** Actual, Unit"
        )
        
        # Sample template
        with st.expander("📄 View CSV Template (All amounts in INR)"):
            st.info("⚠️ **Important:** All financial values must be entered in **Indian Rupees (₹)**. Do NOT use USD or any other currency.")
            sample_csv = """Parameter,Projected,Actual,Unit
Completion Time,12,14,months
Project Budget,50,65,₹ Crore
Units Sold,200,120,units
Cost per Unit,25,32,₹ Lakh
Land Cost,10,12,₹ Crore
Labor Cost,8,9.5,₹ Crore
Material Cost,15,18,₹ Crore"""
            st.code(sample_csv, language="csv")
            st.download_button(
                label="📥 Download CSV Template",
                data=sample_csv,
                file_name="projecttracker_template.csv",
                mime="text/csv"
            )
        
        st.divider()
        
        # File upload
        uploaded_file = st.file_uploader(
            "Choose a CSV file to import",
            type=["csv"],
            help="Select a CSV file with parameter data"
        )
        
        if uploaded_file:
            try:
                df_uploaded = pd.read_csv(uploaded_file)
                
                # Validate
                is_valid, message = validate_project_data(df_uploaded)
                
                if not is_valid:
                    st.error(f"❌ Validation Error: {message}")
                else:
                    st.success("✅ File validated successfully!")
                    
                    st.markdown("### Preview")
                    st.dataframe(df_uploaded, use_container_width=True, hide_index=True)
                    
                    col1, col2 = st.columns([3, 1])
                    with col2:
                        if st.button("🚀 Import Data", use_container_width=True):
                            try:
                                imported_count = 0
                                for idx, row in df_uploaded.iterrows():
                                    param_name = row["Parameter"]
                                    projected = row["Projected"]
                                    unit = row.get("Unit", "") if "Unit" in df_uploaded.columns else ""
                                    actual = row.get("Actual") if "Actual" in df_uploaded.columns else None
                                    
                                    param_id = add_parameter(project_id, param_name, projected, unit)
                                    if actual is not None and pd.notna(actual):
                                        update_actual_value(param_id, actual)
                                    imported_count += 1
                                
                                st.success(f"✅ Successfully imported {imported_count} parameters!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"❌ Import failed: {str(e)}")
            
            except Exception as e:
                st.error(f"❌ Error reading file: {str(e)}")
    
    # ==================== TAB 4: Detailed Analysis ====================
    with tab4:
        st.markdown("## 🔍 Detailed Variance Analysis")
        
        params = get_project_parameters(project_id)
        
        if not params:
            st.info("📭 No parameters to analyze yet.")
        else:
            analyzer = st.session_state.analyzer
            df_analysis = analyzer.analyze_project([
                (p[1], p[2], p[3], p[4], p[0]) for p in params
            ])
            
            if not df_analysis.empty:
                # Filter and sort options
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    show_flagged_only = st.checkbox(
                        "🚨 Show Critical Only",
                        help="Display only parameters with >30% deviation"
                    )
                
                with col2:
                    sort_by = st.selectbox(
                        "Sort by",
                        ["% Deviation (Highest)", "Variance (Largest)", "Parameter (A-Z)"],
                        help="Choose sorting order"
                    )
                
                with col3:
                    show_stats = st.checkbox(
                        "📊 Show Statistics",
                        value=True,
                        help="Display statistical summary"
                    )
                
                # Apply filters
                display_df = df_analysis.copy()
                
                if show_flagged_only:
                    display_df = analyzer.get_flagged_parameters(display_df)
                
                if sort_by == "% Deviation (Highest)":
                    display_df = display_df.reindex(display_df["% Deviation"].abs().sort_values(ascending=False).index)
                elif sort_by == "Variance (Largest)":
                    display_df = display_df.reindex(display_df["Variance"].abs().sort_values(ascending=False).index)
                elif sort_by == "Parameter (A-Z)":
                    display_df = display_df.sort_values("Parameter")
                
                # Format currency columns for display
                display_df_formatted = display_df.copy()
                display_df_formatted['Projected'] = display_df_formatted['Projected'].apply(lambda x: format_for_display(x))
                display_df_formatted['Actual'] = display_df_formatted['Actual'].apply(lambda x: format_for_display(x))
                display_df_formatted['Variance'] = display_df_formatted['Variance'].apply(lambda x: format_for_display(x))
                
                st.divider()
                st.markdown("### Analysis Results")
                st.dataframe(display_df_formatted, use_container_width=True, hide_index=True, height=400)
                
                # Statistics
                if show_stats:
                    st.divider()
                    st.markdown("### 📈 Statistical Summary")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric(
                            "Max Deviation",
                            f"{display_df['% Deviation'].abs().max():.2f}%",
                            help="Highest absolute deviation"
                        )
                    
                    with col2:
                        st.metric(
                            "Min Deviation",
                            f"{display_df['% Deviation'].abs().min():.2f}%",
                            help="Lowest absolute deviation"
                        )
                    
                    with col3:
                        st.metric(
                            "Mean Deviation",
                            f"{display_df['% Deviation'].mean():.2f}%",
                            help="Average deviation"
                        )
                    
                    with col4:
                        st.metric(
                            "Median Deviation",
                            f"{display_df['% Deviation'].abs().median():.2f}%",
                            help="Middle value of deviations"
                        )
                    
                    # Distribution chart
                    fig_dist = px.histogram(
                        display_df,
                        x='% Deviation',
                        nbins=10,
                        title="Deviation Distribution",
                        labels={'% Deviation': 'Deviation %', 'count': 'Number of Parameters'},
                        color_discrete_sequence=['#667eea']
                    )
                    
                    fig_dist.update_layout(
                        height=350,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)',
                        font=dict(family="Arial, sans-serif", size=12),
                        title_font=dict(size=16, color="#333")
                    )
                    
                    st.plotly_chart(fig_dist, use_container_width=True)
    
    # ==================== TAB 5: Help & Documentation ====================
    with tab5:
        st.markdown("## 📞 Help & Documentation")
        
        help_sections = {
            "Getting Started": """
            1. **Create a Project** - Click 'Create Project' in the sidebar
            2. **Add Parameters** - Go to 'Add Parameters' tab and enter your metrics
            3. **Input Data** - Add projected and actual values
            4. **Monitor** - View variance analysis in the Dashboard tab
            """,
            
            "Understanding Deviations": """
            - **🟢 Green (0-15%)** - Within acceptable range
            - **🟡 Orange (15-30%)** - Warning level
            - **🔴 Red (>30%)** - Critical deviation requiring attention
            
            **Formula:** % Deviation = (Actual - Projected) / Projected × 100
            """,
            
            "CSV Import": """
            - Required columns: Parameter, Projected
            - Optional columns: Actual, Unit
            - Download template from the Import tab
            - **All financial values MUST be in Indian Rupees (₹)**
            - Recommended units: ₹ Crore, ₹ Lakh, ₹ (rupees)
            - Ensure numeric values use '.' as decimal separator
            """,
            
            "Export Options": """
            - **CSV** - For Excel and other tools
            - **Excel** - With formatting and multiple sheets
            - **PDF** - Coming soon!
            """,
            
            "Tips & Tricks": """
            - Use descriptive parameter names
            - Keep units consistent (₹ Crore, ₹ Lakh, %, months, etc.)
            - **Always use Indian Rupees (₹) for financial parameters**
            - DO NOT use USD, $ or any other currency
            - 1 Crore = 10 Million Rupees, 1 Lakh = 100,000 Rupees
            - Update actual values regularly
            - Export reports for stakeholder reviews
            - Use the Analysis tab for deep insights
            """
        }
        
        for section, content in help_sections.items():
            with st.expander(f"❓ {section}", expanded=False):
                st.markdown(content)
        
        st.divider()
        
        st.markdown("### 🚀 Need More Help?")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            - Check the README file in the repository
            - Review sample data: `data/sample_project.csv`
            - Contact support for issues
            """)
        
        with col2:
            st.markdown("""
            **Version:** 1.0.0  
            **Last Updated:** 2026-05-28  
            **Developed by:** Rahul STI
            """)


if __name__ == "__main__":
    main()
