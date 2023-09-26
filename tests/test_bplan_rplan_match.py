import os

import numpy as np
import pandas as pd

from data_pipeline.match_RPlan_BPlan.matching_plans import merge_rp_bp

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FOLDER_PATH_TO_SUCCESS = os.path.join(BASE_DIR, "test_data", "test_merge", "success")
SAMPLE_BP_TEST_DF = os.path.join(os.path.dirname(__file__), "test_data", 'test_15__rows.geojson')
REGIONS_DF = os.path.join(os.path.dirname(__file__), "test_data", "regional_plans", "regions_map.geojson")


def test_merge():
    result_df = merge_rp_bp(path_bp_geo=SAMPLE_BP_TEST_DF,
                            path_rp_geo=REGIONS_DF)
    # assert datatypes
    assert isinstance(result_df, pd.DataFrame)
    assert all(result_df[col].dtype == expected_dtype
               for col, expected_dtype in [('unique_id', np.int64),
                                           ('regional_plan_id', np.int64),
                                           ('regional_plan_name', object),
                                           ('ART', object),
                                           ('LND', np.int64)])

    ## Asserts that there are no NA
    assert True not in result_df.isnull()
