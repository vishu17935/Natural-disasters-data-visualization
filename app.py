from dash import Dash, html, dcc, Input, Output, callback_context
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from layout import get_layout  # Import the layout function
from visualizations.viz1 import get_sunburst_viz
from visualizations.viz2 import get_sankey_viz
from visualizations.viz3 import get_bar_viz
from visualizations.viz4 import get_treemap_viz
from visualizations.viz5 import get_stacked_area_viz
from visualizations.viz6 import get_pie_viz
from visualizations.viz7 import get_choropleth_viz

# Initialize the Dash app
app = Dash(__name__, 
           assets_folder="/Users/vishalsingh/python/CS661_dashboard/assets",
           external_stylesheets=['https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css'])

# Load datasets
data_files = {
    'sunburst': "/Users/vishalsingh/python/CS661_dashboard/data/processed/india_gdp_data.csv",
    'sankey': "/Users/vishalsingh/python/CS661_dashboard/data/processed/india_gdp_sankey_data.csv",
    'bar': "/Users/vishalsingh/python/CS661_dashboard/data/processed/india_gdp_bar_data.csv",
    'treemap': "/Users/vishalsingh/python/CS661_dashboard/data/processed/india_gdp_treemap_data.csv",
    'area': "/Users/vishalsingh/python/CS661_dashboard/data/processed/india_gdp_area_data.csv",
    'pie': "/Users/vishalsingh/python/CS661_dashboard/data/processed/india_gdp_pie_data.csv",
    'choropleth': "/Users/vishalsingh/python/CS661_dashboard/data/processed/mapdata.csv"
}

datasets = {}
for name, path in data_files.items():
    try:
        df = pd.read_csv(path)
        if name in ['sunburst', 'treemap']:
            if 'path' not in df.columns:
                print(f"Error: '{path}' missing 'path' column.")
                df = pd.DataFrame()
            else:
                try:
                    df['path'] = df['path'].apply(eval)
                except Exception as e:
                    print(f"Error parsing 'path' in {path}: {str(e)}")
                    df = pd.DataFrame()
        datasets[name] = df
        print(f"Loaded {path} with columns: {df.columns.tolist()}")
    except Exception as e:
        print(f"Error loading {path}: {str(e)}")
        datasets[name] = pd.DataFrame()

# Calculate some KPIs from your data
def calculate_kpis():
    kpis = {}
    if not datasets['pie'].empty:
        total_gdp = datasets['pie']['value'].sum()
        kpis['total_gdp'] = f"${total_gdp:.0f}B"
        kpis['services_percent'] = f"{(datasets['pie'][datasets['pie']['sector'] == 'Services']['value'].iloc[0] / total_gdp * 100):.1f}%"
    
    if not datasets['bar'].empty:
        latest_year = datasets['bar']['year'].max()
        kpis['latest_year'] = latest_year
        kpis['sectors_count'] = len(datasets['bar']['category'].unique())
    
    return kpis

kpis = calculate_kpis()

# Set the app layout
app.layout = get_layout(kpis, datasets)

# Callback for interactive bar chart
@app.callback(
    Output("bar-viz", "figure"),
    Input("year-dropdown", "value")
)
def update_bar_chart(year):
    if year is None or datasets['bar'].empty:
        return px.bar()
    try:
        return get_bar_viz(datasets['bar'], year)
    except Exception as e:
        print(f"Error updating bar chart: {str(e)}")
        return px.bar()

if __name__ == "__main__":
    app.run(debug=True)