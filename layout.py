from dash import html, dcc
from visualizations.viz1 import get_sunburst_viz
from visualizations.viz2 import get_sankey_viz
from visualizations.viz3 import get_bar_viz
from visualizations.viz4 import get_treemap_viz
from visualizations.viz5 import get_stacked_area_viz
from visualizations.viz6 import get_pie_viz
from visualizations.viz7 import get_choropleth_viz

def get_layout(kpis, datasets):
    """
    Defines the layout for the GDP dashboard.

    Parameters:
    - kpis (dict): Dictionary containing KPI values (e.g., total_gdp, services_percent).
    - datasets (dict): Dictionary of DataFrames for visualizations.

    Returns:
    - A Dash HTML Div containing the dashboard layout.
    """
    return html.Div([
        # Sidebar
        html.Div([
            html.Div([
                html.I(className="fas fa-chart-line", style={'fontSize': '24px', 'marginBottom': '10px'}),
                html.H3("GDP DASHBOARD", style={'color': 'white', 'fontSize': '18px', 'fontWeight': 'bold'})
            ], className="sidebar-header"),
            
            html.Div([
                html.Div([
                    html.I(className="fas fa-home sidebar-icon"),
                    html.Span("Dashboard", className="sidebar-text")
                ], className="sidebar-item active"),
                
                html.Div([
                    html.I(className="fas fa-chart-bar sidebar-icon"),
                    html.Span("Analytics", className="sidebar-text")
                ], className="sidebar-item"),
                
                html.Div([
                    html.I(className="fas fa-calendar sidebar-icon"),
                    html.Span("Reports", className="sidebar-text")
                ], className="sidebar-item"),
                
                html.Div([
                    html.I(className="fas fa-cog sidebar-icon"),
                    html.Span("Settings", className="sidebar-text")
                ], className="sidebar-item"),
            ], className="sidebar-menu")
        ], className="sidebar"),
        
        # Main content area
        html.Div([
            # Top header
            html.Div([
                html.H1("India's GDP Dashboard", className="main-title"),
                html.Div([
                    dcc.Input(
                        id="search-input",
                        type="text",
                        placeholder="Search...",
                        className="search-input"
                    ),
                    html.I(className="fas fa-search search-icon"),
                    html.Div([
                        html.I(className="fas fa-bell notification-icon"),
                        html.Span("1", className="notification-badge")
                    ], className="notification-container"),
                    html.Div([
                        html.Span("Admin User", className="user-name"),
                        html.Div(className="user-avatar")
                    ], className="user-info")
                ], className="header-controls")
            ], className="header"),
            
            # KPI Cards Row
            html.Div([
                html.Div([
                    html.Div([
                        html.I(className="fas fa-chart-line kpi-icon", style={'color': '#4CAF50'}),
                        html.Div([
                            html.H3(kpis.get('total_gdp', '$700B'), className="kpi-value"),
                            html.P("Total GDP", className="kpi-label")
                        ], className="kpi-text")
                    ], className="kpi-content")
                ], className="kpi-card kpi-green"),
                
                html.Div([
                    html.Div([
                        html.I(className="fas fa-industry kpi-icon", style={'color': '#2196F3'}),
                        html.Div([
                            html.H3(kpis.get('services_percent', '47%'), className="kpi-value"),
                            html.P("Services Share", className="kpi-label")
                        ], className="kpi-text")
                    ], className="kpi-content")
                ], className="kpi-card kpi-blue"),
                
                html.Div([
                    html.Div([
                        html.I(className="fas fa-calendar kpi-icon", style={'color': '#FF9800'}),
                        html.Div([
                            html.H3(str(kpis.get('latest_year', '2024')), className="kpi-value"),
                            html.P("Latest Year", className="kpi-label")
                        ], className="kpi-text")
                    ], className="kpi-content")
                ], className="kpi-card kpi-orange"),
                
                html.Div([
                    html.Div([
                        html.I(className="fas fa-chart-pie kpi-icon", style={'color': '#9C27B0'}),
                        html.Div([
                            html.H3(str(kpis.get('sectors_count', '3')), className="kpi-value"),
                            html.P("Sectors", className="kpi-label")
                        ], className="kpi-text")
                    ], className="kpi-content")
                ], className="kpi-card kpi-purple")
            ], className="kpi-row"),
            
            # Charts Grid
            html.Div([
                # New row for choropleth map (Position 1)
                html.Div([
                    html.Div([
                        html.Div([
                            html.H4("World Choropleth Map", className="chart-title"),
                            html.I(className="fas fa-expand chart-expand")
                        ], className="chart-header"),
                        dcc.Graph(id="choropleth-viz", figure=get_choropleth_viz(datasets['choropleth']), className="chart-graph")
                    ], className="chart-card large-chart map-chart")
                ], className="chart-row"),
                
                # Row 1: Large charts
                html.Div([
                    html.Div([
                        html.Div([
                            html.H4("GDP by Sector", className="chart-title"),
                            html.I(className="fas fa-expand chart-expand")
                        ], className="chart-header"),
                        dcc.Graph(id="pie-viz", figure=get_pie_viz(datasets['pie']), className="chart-graph")
                    ], className="chart-card large-chart"),
                    
                    html.Div([
                        html.Div([
                            html.H4("GDP Over Time", className="chart-title"),
                            html.I(className="fas fa-expand chart-expand")
                        ], className="chart-header"),
                        dcc.Graph(id="area-viz", figure=get_stacked_area_viz(datasets['area']), className="chart-graph")
                    ], className="chart-card large-chart")
                ], className="chart-row"),
                
                # Row 2: Medium charts
                html.Div([
                    html.Div([
                        html.Div([
                            html.H4("Sector Analysis", className="chart-title"),
                            dcc.Dropdown(
                                id="year-dropdown",
                                options=[{'label': year, 'value': year} for year in datasets['bar']['year'].unique()] if not datasets['bar'].empty else [],
                                value=datasets['bar']['year'].iloc[0] if not datasets['bar'].empty else None,
                                className="chart-dropdown"
                            ),
                            html.I(className="fas fa-expand chart-expand")
                        ], className="chart-header"),
                        dcc.Graph(id="bar-viz", className="chart-graph")
                    ], className="chart-card medium-chart"),
                    
                    html.Div([
                        html.Div([
                            html.H4("GDP Flow", className="chart-title"),
                            html.I(className="fas fa-expand chart-expand")
                        ], className="chart-header"),
                        dcc.Graph(id="sankey-viz", figure=get_sankey_viz(datasets['sankey']), className="chart-graph")
                    ], className="chart-card medium-chart")
                ], className="chart-row"),
                
                # Row 3: Complex visualizations
                html.Div([
                    html.Div([
                        html.Div([
                            html.H4("Hierarchical View", className="chart-title"),
                            html.I(className="fas fa-expand chart-expand")
                        ], className="chart-header"),
                        dcc.Graph(id="sunburst-viz", figure=get_sunburst_viz(datasets['sunburst']), className="chart-graph")
                    ], className="chart-card large-chart"),
                    
                    html.Div([
                        html.Div([
                            html.H4("Treemap Analysis", className="chart-title"),
                            html.I(className="fas fa-expand chart-expand")
                        ], className="chart-header"),
                        dcc.Graph(id="treemap-viz", figure=get_treemap_viz(datasets['treemap']), className="chart-graph")
                    ], className="chart-card large-chart")
                ], className="chart-row")
            ], className="charts-grid")
        ], className="main-content")
    ], className="dashboard-container")