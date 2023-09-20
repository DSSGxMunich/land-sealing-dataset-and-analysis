
import pandas as pd
import re


def enrich_extracts_with_metadata(info_df: pd.DataFrame,
                                  text_df: pd.DataFrame):
    """Function that joins BP-metadata and BP-text to produce the document_texts table.

    Args:
        info_df: df containing metadata
        text_df: df containing extracted text

    Returns:
        final_df: merged df
    """
    # create id columns based on 'filename'
    text_df['document_id'] = text_df['filename'].str.replace(r'\.pdf$', '', regex=True)
    text_df['land_parcel_id'] = text_df['document_id'].str.extract(r'(\d+)')
    
    # merge BP-metadata into BP-text based on objectid
    final_df = pd.merge(text_df, info_df[['objectid', 'name', 'scanurl']],
                        left_on='document_id',
                        right_on='objectid',
                        how='left')
    
    # drop and rename columns
    final_df = final_df.drop(columns=['objectid']).rename(columns={'name': 'land_parcel_name',
                                                                   'scanurl': 'land_parcel_scanurl'})
    
    # reorder columns
    reordered = ['filename', 'document_id', 'content', 'land_parcel_id', 'land_parcel_name', 'land_parcel_scanurl']
    final_df = final_df[reordered + [col for col in final_df.columns if col not in reordered]]

    final_df = final_df.drop_duplicates()

    return final_df
