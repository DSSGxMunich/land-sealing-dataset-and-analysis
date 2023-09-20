import os
import re

import yaml

from data_pipeline.rplan_content_extraction.rplan_content_extractor import RPlanContentExtractor
from data_pipeline.rplan_content_extraction.rplan_utils import CONFIG_FILE_PATH

CHAPTER_TEST_DATA = [
    """Titel
1. Chapter A
1.1 Chapter B
1.2 Chapter C
2. Chapter D
2.1 Chapter E
Content
Chapter B
lorem ipsum
Chapter C
lorem ipsum
Chapter E
lorem ipsum
""",
    """1. Chapter A
1.1 Chapter B
2. Chapter C
2.1 Chapter D
Content
1.1 Chapter A
lorem ipsum
2.1 Chapter D
lorem ipsum
""",
]
_abcd = ['Chapter A', 'Chapter B', 'Chapter C', 'Chapter D']
FULL_CHAPTER_NAMES = [_abcd + ['Chapter E'],
                      _abcd]
FULL_TEXT = ["""
Content
Chapter B
lorem ipsum
Chapter C
lorem ipsum
Chapter E
lorem ipsum
""", """
Content
1.1 Chapter A
lorem ipsum
2.1 Chapter D
lorem ipsum
"""]
INDICES_TEST_DATA = [
    """Chapter
lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum
Ziel: Dont find this
text
Ziel 2 Find this
text
Ziel 3: Find this
text
lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum
""",
    """ lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum
    Grundsatz: Find this
    text
    Grundsatz
    Find this text
    Grundsatz 3: Find this
    text
    Grundsätze:
    Find this text
    diesen grundsatz nicht finden
    """,
    """ lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum lorem ipsum
    Erläuterung: find this text
    Erläuterung 2 Dont find this
    Erläuterung
    Find this text
    Erläuterungen
    Find this text
    dont find this Erläuterungen here
    """,
]


class TestRPlanContentExtractor:
    def setup_class(self):
        self.test_rplan_path = os.path.join(os.path.dirname(__file__), "test_data", "test_rplan", "test_rplan.txt")
        with open(CONFIG_FILE_PATH, 'r', encoding='utf8') as f:
            self.cfg = yaml.load(f, Loader=yaml.FullLoader)
        
        self.rplan_content_extractor = RPlanContentExtractor(self.cfg)

    def test_chapter_names(self):
        # apply function
        for txt, true_chapter_name, true_txt in zip(CHAPTER_TEST_DATA, FULL_CHAPTER_NAMES, FULL_TEXT):
            toc_end = txt.find("Content")
            chapter_names, result_txt = self.rplan_content_extractor.extract_chapter_names(txt=txt,
                                                                                           cfg=self.cfg["format_1"],
                                                                                           toc_end_index=toc_end)
            assert chapter_names == true_chapter_name, f"Expected chapters {true_chapter_name}, got {chapter_names}"
            assert result_txt == true_txt, f"Expected text {true_txt}, got {result_txt}"

    def test_find_chapter_name_for_indices(self):
        correct_chapters = [['Chapter B', 'Chapter C', 'Chapter E'], ['Chapter A', 'Chapter D']]
        for txt, chapter_names, correct_chapter_names in zip(CHAPTER_TEST_DATA, FULL_CHAPTER_NAMES, correct_chapters):
            indices = [match.start() for match in re.finditer(pattern="lorem ipsum", string=txt)]
            found_chapters_for_indices = self.rplan_content_extractor.find_chapter_name_for_indices(txt=txt,
                                                                                                    chapter_names=chapter_names,
                                                                                                    indices=indices)
            assert found_chapters_for_indices == correct_chapter_names, \
                f"Expected chapters {correct_chapter_names}, got {found_chapters_for_indices}"

    def test_parse_into_sections(self):
        txt = ''.join(INDICES_TEST_DATA)
        chapter_names = ["Chapter"]
        sections = self.rplan_content_extractor.parse_into_sections(txt=txt,
                                                                    cfg=self.cfg["format_1"],
                                                                    chapter_names=chapter_names)
        # assert chapter columns contains always "Chapter"
        assert sections["chapter"].unique().tolist() == ["Chapter"], \
            f"Expected chapter column to contain only 'Chapter', got {sections['chapter'].unique().tolist()}"
        # assert that all sections have a chapter name
        assert sections["chapter"].isna().sum() == 0, \
            f"Expected all sections to have a chapter name, got {sections['chapter'].isna().sum()}" \
            f" sections without chapter name"
        true_section_types = ["start"] + ["target"] * 2 + ["principle"] * 3 + ["explanation"] * 3

        assert sections["section_type"].tolist() == true_section_types, \
            f"Expected section types {true_section_types}, got {sections['section_type'].tolist()}"

    def test__get_indices(self):
        correct_indices_list = [[0, 142, 164, 295],
                                [0, 147, 180, 216, 285],
                                [0, 113, 178, 213, 288], ]
        for txt, correct_indices in zip(INDICES_TEST_DATA, correct_indices_list):
            indices, _ = self.rplan_content_extractor._get_indices(txt=txt, indices_cfg=self.cfg["format_1"])
            assert indices == correct_indices, f"Expected indices {correct_indices}, got {indices}"
