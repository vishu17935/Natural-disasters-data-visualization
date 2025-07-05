import pandas as pd
import plotly.express as px

def get_choropleth_viz(data: pd.DataFrame, value_col: str = 'avg deaths by year', location_col: str = 'ISO', hover_name_col: str = 'hovername') -> px.choropleth:
    """
    Creates a choropleth map visualization for world data.

    Parameters:
    - data (pd.DataFrame): A DataFrame with columns for locations, values, and hover names.
    - value_col (str): The column name for the values to color the map by (default: 'avg deaths by year').
    - location_col (str): The column name for the country ISO codes (default: 'ISO').
    - hover_name_col (str): The column name for the country names in hover tooltips (default: 'hovername').

    Returns:
    - A Plotly choropleth figure.
    """
    try:
        # Validate required columns
        required_cols = [location_col, value_col, hover_name_col]
        if not all(col in data.columns for col in required_cols):
            raise ValueError(f"DataFrame must have {', '.join(required_cols)} columns.")
        
        # Validate value column is numerical
        if not pd.api.types.is_numeric_dtype(data[value_col]):
            raise ValueError(f"'{value_col}' column must be numerical.")
        
        # Create choropleth map
        fig = px.choropleth(
            data,
            locations=location_col,
            color=value_col,
            hover_name=hover_name_col,
            color_continuous_scale='Viridis',
            title="World Choropleth Map"
        )
        
        # Update layout
        fig.update_layout(
            margin=dict(t=50, l=25, r=25, b=25),
            title_font_size=20
        )
        
        return fig
    
    except Exception as e:
        print(f"Error creating choropleth map: {str(e)}")
        return px.choropleth()  # Return an empty figure

# Example usage for testing
if __name__ == "__main__":
    # Sample data
    sample_data = pd.DataFrame({
        'ISO': ['USA', 'IND', 'BRA'],
        'hovername': ['United States', 'India', 'Brazil'],
        'colour code': ['A', 'B', 'A'],
        'avg deaths by year': [1000, 2000, 1500],
        'avg economical loss': [500000, 300000, 400000]
    })
    fig = get_choropleth_viz(sample_data)
    fig.show()