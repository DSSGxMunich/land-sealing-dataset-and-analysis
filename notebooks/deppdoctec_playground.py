import cv2
from pathlib import Path
from matplotlib import pyplot as plt
from IPython.core.display import HTML

import deepdoctection as dd

def run_pipeline(pipe, pdf_path):
    df = pipe.analyze(path=pdf_path)
    df.reset_state()
    dp = next(iter(df))
    print(dp.text)


if __name__ == '__main__':
    categories = dd.ModelCatalog.get_profile("fasttext/lid.176.bin").categories
    path_weights = dd.ModelDownloadManager.maybe_download_weights_and_configs("fasttext/lid.176.bin")

    fast_text = dd.FasttextLangDetector(path_weights, categories)
    tess_ocr_config_path = dd.get_configs_dir_path() / "dd/conf_tesseract.yaml"  # This file will be in your .cache if you ran the analyzer before.
    # Otherwise make sure to copy the file from 'configs/conf_tesseract.yaml'

    tesseract_ocr = dd.TesseractOcrDetector(tess_ocr_config_path.as_posix())
    image_path = "/home/jonasklotz/DSSGx/dssgx_land_sealing_dataset_analysis/data/sample.png"

    pdf_path = "/home/jonasklotz/DSSGx/dssgx_land_sealing_dataset_analysis/data/sample2.pdf"

    lang_detect_comp = dd.LanguageDetectionService(fast_text, text_detector=tesseract_ocr)

    pipe_comp_list = [lang_detect_comp]

    order_comp = dd.TextOrderService(text_container=dd.LayoutType.word)
    pipe_comp_list.append(order_comp)

    path_weights = dd.ModelCatalog.get_full_path_weights("layout/d2_model_0829999_layout_inf_only.pt")
    path_configs = dd.ModelCatalog.get_full_path_configs("layout/d2_model_0829999_layout_inf_only.pt")
    categories = dd.ModelCatalog.get_profile("layout/d2_model_0829999_layout_inf_only.pt").categories

    layout_detector = dd.D2FrcnnDetector(path_configs, path_weights, categories, device="cpu")
    layout_comp = dd.ImageLayoutService(layout_detector)

    pipe_comp_list.insert(0, layout_comp)


    tesseract_ocr = dd.TesseractOcrDetector(tess_ocr_config_path.as_posix(), ["LANGUAGES=deu"])
    # setting run_time_ocr_language_selection=True will dynamically select the OCR model for text extraction based on
    # the predicted languages. This helps to get much improved OCR results.rst, if you have documents with various languages.

    text_comp = dd.TextExtractionService(tesseract_ocr, run_time_ocr_language_selection=True)

    map_comp = dd.MatchingService(parent_categories=["text", "title", "list", "table", "figure"],
                                  child_categories=["word"],
                                  matching_rule='ioa', threshold=0.6)  # same setting as for the deepdoctection analyzer

    order_comp = dd.TextOrderService(text_container=dd.LayoutType.word,
                                     floating_text_block_categories=["text", "title", "list", "figure"],
                                     text_block_categories=["text", "title", "list", "table", "figure"])

    #pipe_comp_list = [layout_comp, lang_detect_comp, text_comp, map_comp, order_comp]
    pipe_comp_list = [layout_comp, map_comp, order_comp]

    pipe = dd.DoctectionPipe(pipeline_component_list=pipe_comp_list)

    run_pipeline(pipe, pdf_path)







