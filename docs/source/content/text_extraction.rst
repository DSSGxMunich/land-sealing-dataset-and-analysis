Feature Extraction
------------------------------------------------------------
This section contains the API documentation for the feature extraction, such as the keyword extraction (fuzzy or exact)
and the document categorization.

Document Categorization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This function is a binary categorization of the documents into BP and non-BP documents. It uses the BP keywords and
the BP document structure to detect BP documents.


.. autofunction:: src.features.document_categorization.detecting_BP_and_keywords.run_bp_keyword_detector


Textual Feature Extraction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
This section contains the API documentation for the textual feature extraction, such as the keyword extraction (fuzzy or exact).
The fuzzy keyword extraction is based on the Levenshtein distance and the exact keyword extraction is based on
regular expression or substring matching.

.. autofunction:: src.features.textual_features.document_texts_creation.create_document_texts.enrich_extracts_with_metadata


Fuzzy Keyword Search
#############################################
.. autofunction:: src.features.textual_features.keyword_search.contextual_fuzzy_search.find_best_matches

.. autofunction:: src.features.textual_features.keyword_search.contextual_fuzzy_search.search_df_for_best_matches

.. autofunction:: src.features.textual_features.keyword_search.contextual_fuzzy_search.search_best_matches_dict

.. autofunction:: src.features.textual_features.keyword_search.contextual_fuzzy_search.search_df_for_best_matches_keyword_dict


Exact Keyword Search
#############################################
.. autofunction:: src.features.textual_features.keyword_search.exact_keyword_search.search_text_for_keywords

.. autofunction:: src.features.textual_features.keyword_search.exact_keyword_search.search_df_for_keywords


Agent
#############################################
This section contains the API documentation for the agent extraction. The agent extraction is based on a Large Language Model
and the extraction is done by the GPT-3.5 model. It extracts detailed information from the results of a fuzzy search.
One example would be the extraction of the "Grundflächenzahl" from the sentence "Die Grundflächenzahl beträgt 0,5".

.. warning::
    The agent extraction is not fully evaluated. Even though simple backchecking, e.g. checking if the resulting number
    was actually in the sentence, was done, the extraction is not fully evaluated. The extraction is based on a large
    language model and the results are thus not always correct. One might want to check the results manually before
    using them.



.. autofunction:: src.features.textual_features.knowledge_extraction_agent.agentic_knowledge_extractor.extract_knowledge_from_df


Regional Plan Keyword Search
#############################################

This section contains the API documentation for the regional plan keyword extraction. The regional plan keyword extraction
is based on the regional plan structure and the regional plan keywords. It splits the regional plan into sections and
extracts the keywords from the sections.


.. autofunction:: data_pipeline.rplan_content_extraction.rplan_keyword_search.rplan_exact_keyword_search

.. autofunction:: data_pipeline.rplan_content_extraction.rplan_keyword_search.rplan_fuzzy_keyword_search

.. autofunction:: data_pipeline.rplan_content_extraction.rplan_keyword_search.negate_keyword_search

.. autofunction:: visualizations.rplan_visualization.plot_keyword_search_results




