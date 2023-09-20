import os
import re
from utility.config_utils import read_yaml
import pandas as pd
import yaml
from loguru import logger

from data_pipeline.rplan_content_extraction.rplan_utils import RPLAN_OUTPUT_PATH, RPLAN_TXT_DIR, \
    RPLAN_PDF_DIR, CONFIG_FILE_PATH, parse_result_df, extract_text_and_save_to_txt_files


class RPlanContentExtractor:

    def __init__(self, rplan_config):
        """Initializes the RPlanContentExtractor class.

        Args: rplan_config: the rplan config as dictionary, It contains different format dictionary's e.g. format1
        and format2. Each format dictionary contains the following keys: - chapter_marker: the marker for the
        chapters as string, has to be in a regex format, e.g. Kapitel \d - target_marker: the marker for the targets
        as string, has to be in a regex format, e.g. Ziel \d\n: - principle_marker: the marker for the principles as
        string, has to be in a regex format, e.g. Grundsatz \d\n: - explanation_marker: the marker for the
        explanations as string, has to be in a regex format, e.g. Erläuterung - file_names: list of file names as
        strings, e.g. ['rplan_2019_2024', 'rplan_2020_2025']

            To find the correct format for a rplan, the file name is compared to the file_names list.
            If the file name is in the file_names list, the format is used for the extraction.
            If the file name is not in the file_names list, a ValueError is raised.
            """
        self.rplan_config = rplan_config

    def parse_rplan_from_textfile(self, txt_path: str) -> pd.DataFrame:
        """ Parses a rplan textfile into a dataframe with columns chapter and section

        This method extracts the chapters, targets, principles and explanations from a rplan textfile. The extraction
        is based on the rplan_config.yml file, where regular expressions are given for each rplan and the specific task.
        The textfile is preprocessed before the extraction, e.g. lowered, removal of newlines. The chapters are
        extracted from the first 10% of the textfile, as the chapters are usually listed at the beginning.
        The chapters are then used to assign each section to a chapter.


        Args:
            txt_path: path to the rplan textfile

        Returns:
            sections_df: dataframe with columns filename, chaptername and section


        """
        # read textfile
        filename_without_ext, txt = self.read_text(txt_path)
        cfg = self._get_format_config(filename_without_ext, self.rplan_config)
        toc_marker = self._find_toc_marker(filename_without_ext, txt)

        # # preprocess text
        txt = self.preprocess_rplan_content(txt)

        chapter_names, txt = self.extract_chapter_names(txt, cfg, toc_end_index=toc_marker)
        # split into sections
        sections_df = self.parse_into_sections(txt, cfg, chapter_names)
        sections_df['filename'] = filename_without_ext
        # reorder columns
        sections_df = sections_df[['filename', 'chapter', 'section', 'section_type']]
        return sections_df

    def _find_toc_marker(self, filename_without_ext, txt):
        """Finds the table of contents marker in the textfile.

        The marker is defined in the rplan_config.yml file.
        Args:
            filename_without_ext: the filename without extension
            txt: the rplan content as string

        Returns:
            toc_marker: the index of the table of contents marker
        """
        # get TOC marker
        last_dict, keyword = self.rplan_config['toc_marker'][filename_without_ext]
        if last_dict["last"]:
            toc_marker = txt.rfind(keyword)
        else:
            toc_marker = txt.find(keyword)
        if toc_marker == -1:
            raise ValueError(f"TOC Marker not found in file {filename_without_ext}")
        return toc_marker

    def read_text(self, txt_path):
        with open(txt_path, 'r',encoding='utf8') as f:
            txt = f.read()
        filename = os.path.basename(txt_path)
        filename_without_ext = filename[:filename.rindex('.')]
        return filename_without_ext, txt

    def preprocess_rplan_content(self, content: str):
        """Preprocesses the rplan content

        This method preprocesses the rplan content by removing all whitespaces, newlines and special characters.

        Args:
            content: the rplan content as string

        Returns:
            content: the preprocessed rplan content as string
        """

        # replace   with space
        content = content.replace('\xa0', ' ')

        # convert all multiple whitespaces to single whitespaces
        content = re.sub(' +', ' ', content)

        # remove linebreaks if line contains only whitespace
        content = '\n'.join([line for line in content.split('\n') if line.strip() != ''])

        # remove double linebreaks
        content = content.replace('\n\n', '\n')
        # remove linebreak if line contains only 2 or fewer characters
        content = '\n'.join([line for line in content.split('\n') if len(line) > 2])

        # remove all spaces before or after a newline
        content = content.replace(' \n', '\n').replace('\n ', '\n')

        # remove annoying chars
        chars_to_remove = ['-\n', '–\n', '—\n', '-\n', '- \n', '-', '–', '—', '•', '·', '●', '○', '▪', '▫', '□', '■',
                           '□', '\t']
        for char in chars_to_remove:
            content = content.replace(char, '')

        return content.lower()

    def _find_indices_by_marker(self, content: str, marker: str) -> list:
        """Finds all indices in the content where the marker is located.

        This method finds all indices in the content where the marker is located. The marker is usually a word followed
        by a number, e.g. Ziel 1: or Grundsatz 1:. Unwanted indices are removed, e.g. if the marker is in the middle of
        a word.


        Args:
            content: the rplan content as string
            marker: the marker as string, has to be in a regex format, e.g. Ziel 1\n: or Grundsatz 1\n:
                    markers can be found in the rplan_config.yml file

        Returns:
            indices: list of indices where the marker is located

        """
        # find positions of all marker followed by a number
        if content is None:
            return []
        indices = [m.start() for m in re.finditer(marker, content, flags=re.I)]
        for i, index in enumerate(indices):
            # check if the previous character is a whitespace, newline or newline followed by a whitespace
            if content[index - 1] not in [' ', '\n', '\n ']:
                # if not, remove index
                indices.remove(index)
        # try to remove indices where the marker is in the text
        indices = self._filter_unwanted_prefixes(content, indices)
        return indices

    def _find_explanation_indices(self, content: str, marker: str) -> list:
        """
        Finds all indices in the content where the marker is located.
        
        This method finds all indices in the content where the marker is located. Here, the marker is usually a word
        "Erläuterung". Unwanted indices are removed, e.g. if the marker is in the middle of a word.
        
        
        Args:
            content: the rplan content as string
            marker: the marker as string, has to be in a regex format, e.g. Erläuterung
                    markers can be found in the rplan_config.yml file
                    
        Returns:
            indices: list of indices where the marker is located
        """
        if content is None:
            return []
        explanation_indices = [m.start() for m in re.finditer(marker, content, flags=re.I)]

        explanation_indices = self._filter_unwanted_prefixes(content, explanation_indices)

        return explanation_indices

    def _filter_unwanted_prefixes(self, content, indices, unwanted_prefixes=None):
        """Removes indices where the marker right after a conjunction, e.g. "oder" or "und".

        This method removes indices where the marker right after a conjunction, e.g. "oder" or "und".

        Args:
            content: the rplan content as string
            indices: list of indices where the marker is located
            unwanted_prefixes: list of prefixes that should be removed, e.g. ["oder", "und"]

        Returns:
            indices: list of indices where the marker is located
        """
        if unwanted_prefixes is None:
            unwanted_prefixes = ['zu', 'oder', 'und', 'nach']
        for index in indices:
            for prefix in unwanted_prefixes:
                if prefix in content[index - (len(prefix) + 3):index]:
                    indices.remove(index)
        return indices

    def parse_into_sections(self, txt: str, cfg: dict, chapter_names: list) -> pd.DataFrame:
        """Parses the rplan content into sections.

        This method parses the rplan content into sections. The sections are the targets, principles and explanations.
        The indices of the sections are found by the markers, which are defined in the rplan_config.yml file.
        The chapters are used to assign each section to a chapter.

        Args:
            txt: the rplan content as string
            cfg: the rplan config as dictionary, for keys of the dict see init method
            chapter_names: list of chapter names as strings

        Returns:
            result_df: dataframe with columns chapter and section
        """

        indices, section_types = self._get_indices(cfg, txt)
        # assign chapter name to index
        closest_chapter_names = self.find_chapter_name_for_indices(indices, chapter_names, txt)
        closest_chapter_names = closest_chapter_names[1:]  # remove start section
        sections = [txt[indices[i]:indices[i + 1]] for i in range(len(indices) - 1)]
        result_df = pd.DataFrame({'chapter': closest_chapter_names, 'section': sections, 'section_type': section_types})
        return result_df

    def find_chapter_name_for_indices(self, indices, chapter_names, txt):
        """Finds the chapter name for each index."""
        closest_chapter_names = []
        for index in indices:
            closest_chapter_names.append(self._find_closest_chapter_name(index, chapter_names, txt))
        return closest_chapter_names

    def _get_indices(self, indices_cfg: dict, txt: str):
        """Gets the indices for the targets, principles and explanations."""
        # get indices
        principles_indices = self._find_indices_by_marker(txt, marker=indices_cfg['principle_marker'])
        target_indices = self._find_indices_by_marker(txt, marker=indices_cfg['target_marker'])
        explanation_indices = self._find_explanation_indices(txt, marker=indices_cfg['explanation_marker'])
        section_type = ["principle"] * len(principles_indices) + ["target"] * len(target_indices) + [
            "explanation"] * len(explanation_indices)

        # combine indices
        combined_indices = principles_indices + target_indices + explanation_indices
        # sort sectiontypes based on indices
        sorted_section_type = [x for _, x in sorted(zip(combined_indices, section_type))]
        sorted_section_type = ['start'] + sorted_section_type  # add start section that has no type
        indices = sorted(combined_indices)
        # add start and end index
        indices = [0] + indices + [len(txt)]
        return indices, sorted_section_type

    def _get_format_config(self, filename, indices_cfg):
        """Gets the format config for the given filename."""
        for format_key, format_cfg in indices_cfg.items():
            if "file_names" in format_cfg.keys() and filename in format_cfg["file_names"]:
                indices_cfg = format_cfg
                return indices_cfg
        raise ValueError(f"Format for file {filename} not found, maybe it's not in the config file?")

    def extract_chapter_names(self, txt, cfg, margin: float = 0.1, toc_end_index: int = None):
        """Extracts the chapter names from the textfile.

        This method extracts the chapter names from the textfile. The chapter names are usually listed at the beginning
        of the textfile, therefore the margin. The chapter names are used to assign each section to a chapter.


        Args:
            txt: the rplan content as string
            cfg: the rplan config as dictionary, for keys of the dict see init method
            margin: the margin as float, the chapter names are extracted from the first margin% of the textfile. Not
                    used if toc_end_index is specified
            toc_end_index: the index where the table of contents ends, if None, the margin is used

        Returns:
            chapter_names: list of chapter names as strings
            txt: the rplan content as string
        """
        if toc_end_index:
            starting_text = txt[:toc_end_index]
        else:
            starting_text = txt[:int(len(txt) * margin)]

        chapter_marker = cfg['chapter_marker']
        complete_chapternames = [line for line in starting_text.split('\n') if re.match(chapter_marker, line)]

        # remove all numbers and dots from the chapters
        chapter_names = [re.sub('\d', '', chapter) for chapter in complete_chapternames]
        chapter_names = [re.sub('\.', '', chapter) for chapter in chapter_names]
        # remove trailing whitespaces
        chapter_names = [chapter.strip() for chapter in chapter_names]
        # remove empty chapters
        chapter_names = [chapter for chapter in chapter_names if chapter != '']
        # remove complete chapter names that are not in the chapters
        chapter_names = list(dict.fromkeys(chapter_names))  # remove doubles
        txt = txt[txt.find(chapter_names[-1], 1) + len(chapter_names[-1]):]

        return chapter_names, txt

    def _find_closest_chapter_name(self, index, chapter_names, txt):
        """Finds the closest chapter name for a given index."""
        closest_chapter_name = ""
        closest_position = -1  # set to high number
        for i, chapter_name in enumerate(chapter_names):
            tmp_position = txt.rfind(chapter_name, 0, index)
            # if chapter not found -1 is returned and always smaller than closest_position
            if tmp_position > closest_position:  # chapter name found and closer than previous chapter name
                closest_chapter_name = chapter_name
                closest_position = tmp_position
        return closest_chapter_name


def parse_rplan_directory(txt_dir_path: str, json_output_path: str = None):
    """Parses a directory with rplan textfiles into a dataframe with columns chapter and section

    This method extracts the chapters, targets, principles and explanations from a rplan textfile. The extraction
    is based on the rplan_config.yml file, where regular expressions are given for each rplan and the specific task.
    The textfile is preprocessed before the extraction, e.g. lowered, removal of newlines. The chapters are
    extracted from the first 10% of the textfile, as the chapters are usually listed at the beginning.
    The chapters are then used to assign each section to a chapter. The dataframe is then saved to a json file.

    Args:
        txt_dir_path: path to the directory with the rplan textfiles
        json_output_path: path to the output json file

    Returns:
        sections_df: dataframe with columns filename, chapter and section

    """

    cfg = read_yaml(CONFIG_FILE_PATH)

    rplan_content_extractor = RPlanContentExtractor(cfg)

    df_list = []
    # iterate over all files in folder
    for filename in os.listdir(txt_dir_path):
        txt_path = os.path.join(txt_dir_path, filename)
        logger.debug(txt_path)
        if os.path.isfile(txt_path):
            logger.debug(f"Processing file {txt_path}")
            try:
                result_df = rplan_content_extractor.parse_rplan_from_textfile(txt_path)
            except ValueError as e:
                logger.error(f"Skipping file {txt_path} due to error {e}")
                continue
            df_list.append(result_df)
        else:
            logger.warning(f"Skipping file {txt_path} as it is not a file")

    result_df = pd.concat(df_list).reset_index(drop=True)
    if json_output_path is not None:
        # save df as JSON
        result_df.to_json(json_output_path)
        logger.info(f"Parsing done. Saved to {json_output_path}")
    return result_df


def parse_pdf_dir():
    """ Parses the rplan pdfs in the rplan pdf directory and saves the result as json file.

    The file paths are specified in the rplan_utils.py file.
    """
    extract_text_and_save_to_txt_files(pdf_dir_path=RPLAN_PDF_DIR)
    result_df = parse_rplan_directory(txt_dir_path=RPLAN_TXT_DIR, json_output_path=RPLAN_OUTPUT_PATH)
    result_df = parse_result_df(df=result_df)
    # save df as JSON
    result_df.to_json(RPLAN_OUTPUT_PATH)
    logger.info(f"Parsing done. Saved to {RPLAN_OUTPUT_PATH}")


if __name__ == '__main__':
    result_df = parse_rplan_directory(txt_dir_path=RPLAN_TXT_DIR, )
    # df = parse_result_df(df=result_df)
