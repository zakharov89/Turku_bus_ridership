import pandas as pd

def load_clean_data(trips_csv, stops_json):

    """
    Load, clean, and merge trips and stops data.

    Args:
        trips_csv (str | Path): Path to the trips CSV file (semicolon-delimited).
        stops_json (str | Path): Path to the stops JSON file.

    Returns:
        ext_data (pd.DataFrame): merged dataset with stop metadata and placeholder names.
        data (pd.DataFrame): original cleaned trips data.
        stops (pd.DataFrame): cleaned stops table.
        missing_stops (list): list of stop IDs not found in stops.json.
    """

    # Load trips data
    data = pd.read_csv(trips_csv, sep=';')
    data['date'] = pd.to_datetime(data['date'], format='%d.%m.%Y', errors="coerce")
    
    # Load and prepare stops data
    stops_dict = pd.read_json(stops_json).to_dict()
    stops = pd.DataFrame.from_dict(stops_dict, orient='index').reset_index()
    stops.rename(columns={"index": "stop_id"}, inplace=True)
    if 'stop_code' in stops.columns:
        stops.drop(columns="stop_code", inplace=True)
   
    # Merge trips and stops
    ext_data = data.merge(stops, how='left', left_on='stop', right_on='stop_id')
    ext_data.drop(columns="stop_id", inplace=True)

    # Identify missing stops
    missing_data = ext_data[ext_data['stop_name'].isna()]
    missing_stops = missing_data['stop'].unique().tolist()
  
    # Fill NaNs with placeholder
    ext_data['stop_name_filled'] = ext_data['stop_name'].fillna('Unknown Stop')
   
    return ext_data, data, stops, missing_stops

