Feature Extraction
------------------------------------------------------------
This section contains the API documentation for the feature extraction, such as the keyword extraction (fuzzy or exact)
and the document categorization.

Document Categorization
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autofunction:: src.features.document_categorization.detecting_BP_and_keywords.run_bp_keyword_detector


Textual Feature Extraction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
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
.. autofunction:: src.features.textual_features.knowledge_extraction_agent.agentic_knowledge_extractor.extract_knowledge_from_df
