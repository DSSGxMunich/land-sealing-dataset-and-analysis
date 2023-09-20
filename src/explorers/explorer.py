import pandas as pd
import geopandas as gpd
import os

def land_parcels(input_filepath="data/nrw/land_parcels.geojson"):
    land_parcels_gdf = gpd.read_file(input_filepath)
    land_parcels_gdf = land_parcels_gdf.rename(
        columns={'objectid': 'Land Parcel ID', 
                 'regional_plan_id': 'Region Plan ID'}
    )
    return land_parcels_gdf

def document_texts(input_filepath="data/document_texts/nrw_document_texts.csv", 
                   sample_n=None,
                   usecols=None):
    if input_filepath.endswith('.csv'):
        df = pd.read_csv(
            input_filepath,
            nrows=sample_n,
        )
    elif input_filepath.endswith('.json'):
        df = pd.read_json(input_filepath)
    else:
        raise ValueError(
            "Unsupported file format. Only CSV and JSON files are supported.")
    df = df.rename(columns={'land_parcel_id': 'Land Parcel ID'})
    return df

def regional_plans(input_filepath=
                   "data/NRW/extracted_rplan_content.json"):
    # Check the file extension to determine the format and 
    # read accordingly
    if input_filepath.endswith('.csv'):
        df = pd.read_csv(input_filepath)
    elif input_filepath.endswith('.json'):
        df = pd.read_json(input_filepath)
    else:
        raise ValueError("Unsupported file format. Only CSV and JSON files are supported.")
    
    df = df.rename(columns={'PLR': 'Region Plan ID'})
    return df

def exact_keyword(input_filepath="data/NRW/features/exact_seach/exact_search_final.csv"):
    if input_filepath.endswith('.csv'):
        df = pd.read_csv(input_filepath)
    elif input_filepath.endswith('.json'):
        df = pd.read_json(input_filepath)
    else:
        raise ValueError("Unsupported file format. Only CSV and JSON files are supported.")
    
    # Convert all columns (except 'filename') to boolean (True if not missing, False if missing)
    for col in df.columns:
        if col != 'filename':
            df[col] = df[col].notna()
    
    return df

def fuzzy_keyword(input_folder_path="data/keyword_search/fuzzy_search/75_20"):
    concatenated_dfs = []
    
    for root, dirs, files in os.walk(input_folder_path):
        for file in files:
            if file.endswith(".csv"):
                file_path = os.path.join(root, file)
                csv_df = pd.read_csv(file_path)
                concatenated_dfs.append(csv_df)

    if not concatenated_dfs:
        return None
    
    concatenated_df = pd.concat(concatenated_dfs, 
                                ignore_index=True, sort=False)
    concatenated_df.rename(columns={"id": "Document ID"}, inplace=True)

    return concatenated_df

def knowledge_agent(input_filename=
                    "data/NRW/knowledge_agent_output.json"):

    if input_filename.endswith('.csv'):
        return pd.read_csv(input_filename)
    elif input_filename.endswith('.json'):
        return pd.read_json(input_filename)
    else:
        raise ValueError("Unsupported file format.Only CSV and JSON files are supported.")