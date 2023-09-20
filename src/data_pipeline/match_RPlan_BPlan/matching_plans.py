import geopandas as gpd



def _proc_bp_geo_for_merge(path_bp_geo='../data/NRW/NRW_BP.geojson'):
    """ Process the BP geojson file for merging."""
    bplan_gdf = gpd.read_file(path_bp_geo)

    # Set correct CRS
    bplan_gdf = bplan_gdf.to_crs(epsg=4326)

    # Dissolve one BP into the same geometry, to save memory
    bplan_gdf = bplan_gdf.dissolve(by='objectid')

    bplan_gdf = bplan_gdf.reset_index()

    # Removing duplicates
    bplan_gdf = bplan_gdf.drop_duplicates()

    bplan_gdf = bplan_gdf.rename(columns={'objectid': 'unique_id'})

    return bplan_gdf


def _process_r_plans_for_merge(path_rp_geo='../data/regional_plans/regions_map.geojson'):
    """ Process the RP geojson file for merging."""
    regional_plans = gpd.read_file(path_rp_geo)

    nrw_regions = regional_plans[(regional_plans['LND'] == 5)]

    # renaming columns so they are readable
    nrw_regions = nrw_regions.rename(columns={"PLR": "regional_plan_id", "Name": "regional_plan_name"})

    return nrw_regions


def merge_rp_bp(path_bp_geo='../data/NRW/NRW_BP.geojson',
                path_rp_geo='../data/regional_plans/regions_map.geojson') -> 'gpd.GeoDataFrame':
    """ Merge the BP and RP geojson files into one .

    Args:
        path_bp_geo: path to the BP geojson file
        path_rp_geo: path to the RP geojson file

    Returns:
        gpd.GeoDataFrame: GeoDataFrame with the overlapped BP and RP geojson files
    """
    BP_ID = _proc_bp_geo_for_merge(path_bp_geo)

    nrw_regions = _process_r_plans_for_merge(path_rp_geo)

    bp_merged_regions_geo = gpd.sjoin(BP_ID, nrw_regions, how='inner')

    bp_merged_regions_geo = bp_merged_regions_geo.drop(columns={'index_right', 'id'})

    bp_merged_regions_geo = bp_merged_regions_geo.drop_duplicates()

    return bp_merged_regions_geo


def export_merged_bp_rp(output_path,
                        path_bp_geo='../data/NRW/NRW_BP.geojson',
                        path_rp_geo='../data/regional_plans/regions_map.geojson'):
    """ Export the merged BP and RP geojson files into one .
    Wrapper function for merge_rp_bp

    Args:
        output_path: path to the output file
        path_bp_geo: path to the BP geojson file
        path_rp_geo: path to the RP geojson file

    Returns:
        gpd.GeoDataFrame: GeoDataFrame with the overlapped BP and RP geojson files
    """
    merged_bp_rp = merge_rp_bp(path_bp_geo, path_rp_geo)

    merged_bp_rp.to_file(output_path, driver='GeoJSON')

    return merged_bp_rp
