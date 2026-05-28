"""
ProjectTracker - Real Estate Variance Analysis Dashboard
Main Streamlit Application
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

# Page configuration
st.set_page_config(
    page_title="ProjectTracker - Variance Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .deviation-flag {
        background-color: #ffebee;
        padding: 15px;
        border-left: 5px solid #f44336;
        border-radius: 5px;
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


def main():
    """Main application"""
    initialize_app()
    
    # Header
    st.markdown("# 📊 ProjectTracker - Real Estate Variance Analysis")
    st.markdown("**Monitor projected vs actual parameters with 30% deviation flagging**")
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🚀 Project Navigation")
        
        # Project selection
        projects = get_all_projects()
        project_names = [p[1] for p in projects] if projects else []
        
        selected_project = st.selectbox(
            "Select Project",
            options=project_names if project_names else [""],
            key="project_selector"
        )
        
        # Get selected project ID
        if selected_project and projects:
            st.session_state.current_project_id = next(
                (p[0] for p in projects if p[1] == selected_project), None
            )
        
        st.divider()
        
        # Create new project
        st.markdown("### ➕ New Project")
        new_project_name = st.text_input("Project Name", placeholder="e.g., Residential Complex A")
        new_project_desc = st.text_area("Description", placeholder="Project details", height=80)
        new_project_date = st.date_input("Start Date")
        
        if st.button("Create Project", use_container_width=True):
            if new_project_name.strip():
                project_id = add_project(
                    new_project_name,
                    new_project_desc,
                    str(new_project_date)
                )
                if project_id:
                    st.success(f"✅ Project '{new_project_name}' created!")
                    st.session_state.refresh = True
                    st.rerun()
                else:
                    st.error("❌ Project name already exists!")
            else:
                st.warning("⚠️ Please enter a project name")
    
    # Main content area
    if not st.session_state.current_project_id:
        st.info("👈 Select or create a project from the sidebar to begin")
        return
    
    # Get current project details
    projects = get_all_projects()
    current_project = next(
        (p for p in projects if p[0] == st.session_state.current_project_id), None
    )
    
    if not current_project:
        st.error("Project not found")
        return
    
    project_id, project_name, project_desc, project_date = current_project
    
    # Project header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"### {project_name}")
        if project_desc:
            st.caption(project_desc)
    
    st.divider()
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(
        ["📈 Dashboard", "➕ Add Parameters", "📥 Upload CSV", "📊 Analysis"]
    )
    
    # ==================== TAB 1: Dashboard ====================
    with tab1:
        st.markdown("## Variance Dashboard")
        
        # Get parameters
        params = get_project_parameters(project_id)
        
        if not params:
            st.info("No parameters added yet. Use the 'Add Parameters' tab to get started.")
        else:
            # Analyze variance
            analyzer = st.session_state.analyzer
            df_analysis = analyzer.analyze_project([
                (p[1], p[2], p[3], p[4], p[0]) for p in params
            ])
            
            if not df_analysis.empty:
                # Summary metrics
                summary = analyzer.generate_summary(df_analysis)
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Parameters", summary["total_parameters"])
                with col2:
                    st.metric(
                        "🚨 Major Deviations",
                        summary["flagged_count"],
                        delta=f"{(summary['flagged_count']/summary['total_parameters']*100):.1f}%"
                    )
                with col3:
                    st.metric("✅ OK", summary["ok_count"])
                with col4:
                    st.metric(
                        "Avg Deviation",
                        f"{summary['avg_deviation']:.2f}%"
                    )
                
                st.divider()
                
                # Variance table
                st.markdown("### Parameter Analysis")
                display_df = df_analysis.copy()
                st.dataframe(display_df, use_container_width=True, hide_index=True)
                
                # Flagged deviations alert
                flagged_df = analyzer.get_flagged_parameters(df_analysis)
                if not flagged_df.empty:
                    st.warning(f"⚠️ {len(flagged_df)} Major Deviation(s) Detected")
                    with st.expander("View Flagged Parameters", expanded=True):
                        for idx, row in flagged_df.iterrows():
                            st.markdown(
                                f"**{row['Parameter']}** | "
                                f"Projected: {row['Projected']} {row['Unit']} → "
                                f"Actual: {row['Actual']} {row['Unit']} | "
                                f"{row['% Deviation']:.2f}%",
                                help=f"Deviation: {row['Variance']:.2f}"
                            )
                
                # Visualizations
                st.divider()
                st.markdown("### Visualization")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Projected vs Actual comparison
                    fig_comp = go.Figure(data=[
                        go.Bar(name='Projected', x=df_analysis['Parameter'], y=df_analysis['Projected']),
                        go.Bar(name='Actual', x=df_analysis['Parameter'], y=df_analysis['Actual'])
                    ])
                    fig_comp.update_layout(
                        title="Projected vs Actual Values",
                        barmode='group',
                        height=400,
                        hovermode='x unified'
                    )
                    st.plotly_chart(fig_comp, use_container_width=True)
                
                with col2:
                    # Deviation chart
                    colors = ['red' if abs(x) > 30 else 'green' for x in df_analysis['% Deviation']]
                    fig_dev = go.Figure(data=[
                        go.Bar(
                            x=df_analysis['Parameter'],
                            y=df_analysis['% Deviation'],
                            marker_color=colors,
                            marker_line_color='darkred',
                            marker_line_width=1.5
                        )
                    ])
                    fig_dev.add_hline(y=30, line_dash="dash", line_color="red", annotation_text="30% Threshold")
                    fig_dev.add_hline(y=-30, line_dash="dash", line_color="red")
                    fig_dev.update_layout(
                        title="% Deviation from Projection",
                        yaxis_title="Deviation %",
                        height=400,
                        hovermode='x'
                    )
                    st.plotly_chart(fig_dev, use_container_width=True)
                
                # Export options
                st.divider()
                col1, col2 = st.columns(2)
                
                with col1:
                    csv = df_analysis.to_csv(index=False)
                    st.download_button(
                        label="📥 Download CSV",
                        data=csv,
                        file_name=f"{project_name}_variance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
                
                with col2:
                    # Excel export
                    excel_buffer = io.BytesIO()
                    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
                        df_analysis.to_excel(writer, index=False)
                    excel_buffer.seek(0)
                    st.download_button(
                        label="📊 Download Excel",
                        data=excel_buffer,
                        file_name=f"{project_name}_variance_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
    
    # ==================== TAB 2: Add Parameters ====================
    with tab2:
        st.markdown("## Add Project Parameters")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            param_name = st.text_input("Parameter Name", placeholder="e.g., Completion Time")
        with col2:
            param_projected = st.number_input("Projected Value", value=0.0, step=0.01)
        with col3:
            param_unit = st.text_input("Unit", placeholder="e.g., months, ₹ Cr", max_chars=20)
        with col4:
            param_actual = st.number_input("Actual Value (Optional)", value=None)
        
        if st.button("Add Parameter", use_container_width=True):
            if param_name.strip():
                param_id = add_parameter(project_id, param_name, param_projected, param_unit)
                if param_actual is not None:
                    update_actual_value(param_id, param_actual)
                st.success("✅ Parameter added!")
                st.rerun()
            else:
                st.error("❌ Please enter parameter name")
        
        st.divider()
        
        # Show existing parameters
        st.markdown("### Current Parameters")
        params = get_project_parameters(project_id)
        
        if params:
            for param_id, param_name, projected, actual, unit in params:
                col1, col2, col3, col4, col5 = st.columns([2, 1.5, 1.5, 1, 1])
                
                with col1:
                    st.text(param_name)
                with col2:
                    st.text(f"Proj: {projected} {unit}")
                with col3:
                    if actual is not None:
                        st.text(f"Act: {actual} {unit}")
                    else:
                        st.text("Act: -")
                with col4:
                    new_actual = st.number_input(
                        "Update Actual",
                        value=actual if actual is not None else 0.0,
                        key=f"actual_{param_id}",
                        label_visibility="collapsed"
                    )
                with col5:
                    if st.button("Update", key=f"update_{param_id}", use_container_width=True):
                        update_actual_value(param_id, new_actual)
                        st.success("✅ Updated!")
                        st.rerun()
        else:
            st.info("No parameters yet. Add one above!")
    
    # ==================== TAB 3: Upload CSV ====================
    with tab3:
        st.markdown("## Upload Project Data (CSV)")
        st.info(
            "📋 Required columns: **Parameter**, **Projected** \n"
            "Optional columns: **Actual**, **Unit**"
        )
        
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        
        if uploaded_file:
            try:
                df_uploaded = pd.read_csv(uploaded_file)
                
                # Validate
                is_valid, message = validate_project_data(df_uploaded)
                
                if not is_valid:
                    st.error(f"❌ Validation failed: {message}")
                else:
                    st.success("✅ File validated successfully")
                    st.dataframe(df_uploaded, use_container_width=True)
                    
                    if st.button("Import Data into Project", use_container_width=True):
                        for idx, row in df_uploaded.iterrows():
                            param_name = row["Parameter"]
                            projected = row["Projected"]
                            unit = row.get("Unit", "") if "Unit" in row else ""
                            actual = row.get("Actual") if "Actual" in row else None
                            
                            param_id = add_parameter(project_id, param_name, projected, unit)
                            if actual is not None and pd.notna(actual):
                                update_actual_value(param_id, actual)
                        
                        st.success(f"✅ Imported {len(df_uploaded)} parameters!")
                        st.rerun()
            
            except Exception as e:
                st.error(f"❌ Error reading file: {str(e)}")
    
    # ==================== TAB 4: Detailed Analysis ====================
    with tab4:
        st.markdown("## Detailed Variance Analysis")
        
        params = get_project_parameters(project_id)
        
        if not params:
            st.info("No parameters to analyze yet.")
        else:
            analyzer = st.session_state.analyzer
            df_analysis = analyzer.analyze_project([
                (p[1], p[2], p[3], p[4], p[0]) for p in params
            ])
            
            if not df_analysis.empty:
                # Filter options
                col1, col2 = st.columns(2)
                
                with col1:
                    show_flagged_only = st.checkbox("Show Major Deviations Only")
                
                with col2:
                    sort_by = st.selectbox(
                        "Sort by",
                        ["% Deviation (Highest)", "Variance (Largest)", "Parameter (A-Z)"]
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
                
                st.dataframe(display_df, use_container_width=True, hide_index=True)
                
                # Statistics
                st.markdown("### Statistics")
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(
                        "Max Deviation",
                        f"{display_df['% Deviation'].abs().max():.2f}%"
                    )
                with col2:
                    st.metric(
                        "Min Deviation",
                        f"{display_df['% Deviation'].abs().min():.2f}%"
                    )
                with col3:
                    st.metric(
                        "Median Deviation",
                        f"{display_df['% Deviation'].abs().median():.2f}%"
                    )


if __name__ == "__main__":
    main()
