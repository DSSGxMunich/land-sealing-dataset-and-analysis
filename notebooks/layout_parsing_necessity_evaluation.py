import os
import json
from collections import defaultdict

import pandas as pd

from src.pdf_scraper.tika_pdf_scraper import pdf_parser_from_folder, write_to_csv, pdf_parser_from_path
import cv2
import csv

from features.OCR.preprocessing.image_extractor import slice_bbox_from_image


def find_pdf_for_image_folder(img_dir, pdf_dir, output_dir):
    """ Find all pdfs with the same filename as the images in img_dir and copy them to output_dir.
    """
    img_files = os.listdir(img_dir)
    # get all filenames
    img_filenames = [os.path.splitext(img_file)[0] for img_file in img_files]
    pdf_file_names = [pdf_dir + '/' + img_filename + ".pdf" for img_filename in img_filenames]
    print(pdf_file_names)

    for pdf_file_name in pdf_file_names:
        if os.path.isfile(pdf_file_name):
            os.system("cp " + pdf_file_name + " " + output_dir)
        else:
            print("Could not find file: " + pdf_file_name)


def load_annotation_bboxes(annotations_path):
    with open(annotations_path, 'r') as f:
        results = json.load(f)
    # get all bounding boxes
    bboxes = defaultdict(list)
    for img_dict in results["images"]:
        file_name = img_dict["file_name"].split("/")[-1]

        id = img_dict["id"]
        for annotation in results["annotations"]:
            if annotation["image_id"] == id:
                bbox = annotation["bbox"]
                bboxes[file_name].append(bbox)

    return bboxes


def extract_and_save_bboxes(img_dir, output_dir, bboxes):
    """ Extract all bounding boxes from images in img_dir and save them in output_dir.
    """
    img_files = os.listdir(img_dir)
    # get all filenames
    for img_file in img_files:
        img = cv2.imread(img_dir + "/" + img_file)
        for index, bbox in enumerate(bboxes[img_file]):
            new_path = output_dir + "/" + img_file.split(".")[0] + "_" + str(index) + ".jpg"
            img_bbox = slice_bbox_from_image(img, bbox)
            try:
                # if file already exists, skip
                if os.path.isfile(new_path):
                    continue
                cv2.imwrite(new_path, img_bbox)
            except:
                print("Could not save image: " + new_path)
                continue


def get_files_in_other_dir(df, dir):
    # get col 0
    file_names = df.iloc[:, 0]
    # get all unique values
    unique_file_names = list(file_names.unique())
    # remove ending
    unique_file_names = [x.split(".")[0] for x in unique_file_names]
    # get names of all images
    files = os.listdir(dir)
    # filter images that are in file names
    files = [x for x in files if x.split(".")[0] in unique_file_names]
    # get complete path
    files = [dir + "/" + x for x in files]
    return files


def create_dfs():
    img_dir = "/home/jonasklotz/DSSGx/dssgx_land_sealing_dataset_analysis/data/labelled_data/images"
    pdf_dir = "/home/jonasklotz/DSSGx/dssgx_land_sealing_dataset_analysis/data/nrw/train_set/pdfs"
    output_dir = "/home/jonasklotz/DSSGx/dssgx_land_sealing_dataset_analysis/data/labelled_data/pdfs"
    cut_dir = "/home/jonasklotz/DSSGx/dssgx_land_sealing_dataset_analysis/data/labelled_data/cutted"

    annotations_path = "/home/jonasklotz/DSSGx/dssgx_land_sealing_dataset_analysis/data/labelled_data/result.json"
    find_pdf_for_image_folder(img_dir, pdf_dir, output_dir)

    bboxes = load_annotation_bboxes(annotations_path)
    print(bboxes)
    extract_and_save_bboxes(img_dir, cut_dir, bboxes)

    parsed_pdfs = pdf_parser_from_folder(output_dir)
    # convert to df
    parsed_pdfs_df = pd.DataFrame(parsed_pdfs)
    pdf_csv_path = "/home/jonasklotz/DSSGx/dssgx_land_sealing_dataset_analysis/data/labelled_data/parsed_pdfs.csv"
    # write to csv
    write_to_csv(parsed_pdfs_df, pdf_csv_path)

    # read csv no header
    df = pd.read_csv(pdf_csv_path, header=None)
    #
    img_files = get_files_in_other_dir(df, img_dir)
    contents = []
    for img_path in img_files:
        content_dict = pdf_parser_from_path(img_path)
        contents.append(content_dict["content"])
    # # append to df
    df["2"] = contents
    #
    img_and_pdf_csv_path = "/home/jonasklotz/DSSGx/dssgx_land_sealing_dataset_analysis/data/labelled_data/parsed_pdfs_with_img.csv"
    # # write to csv
    with open(img_and_pdf_csv_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        for index, row in df.iterrows():
            csv_writer.writerow([row.iloc[0], row.iloc[1], row.iloc[2]])


    # read csv no header
    df = pd.read_csv(img_and_pdf_csv_path, header=None)
    # remove 2406001_10.pdf
    df = df[df.iloc[:, 0] != "2406001_10.pdf"]
    # get col 0
    file_names = df.iloc[:, 0]
    grouped_cut_files = defaultdict(list)
    for file_name in file_names:
        for cut_file in os.listdir(cut_dir):
            if cut_file.startswith(file_name.split(".")[0]):
                grouped_cut_files[file_name].append(cut_file)

    all_contents = []
    # iterate over keys
    for key in grouped_cut_files.keys():
        # parse pdf and concat all contents
        content = ""
        g_cut_files = sorted(grouped_cut_files[key], key=lambda x: int(x.split("_")[-1].split(".")[0]))
        for cut_file in g_cut_files:
            content_dict = pdf_parser_from_path(cut_dir + "/" + cut_file)
            content += content_dict["content"] if content_dict["content"] else ""
        all_contents.append(content)

    # append to df
    print(len(all_contents))
    df["3"] = all_contents
    cut_img_and_pdf_csv_path = "/home/jonasklotz/DSSGx/dssgx_land_sealing_dataset_analysis/data/labelled_data/parsed_pdfs_with_img_and_cut.csv"

    # write to csv
    with open(cut_img_and_pdf_csv_path, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        for index, row in df.iterrows():
            csv_writer.writerow([row.iloc[0], row.iloc[1], row.iloc[2], row.iloc[3]])


def get_meaningful_word_count(content, model):
    # split content into words
    words = content.split(" ")
    # remove empty strings
    words = [x for x in words if x]
    # remove stopwords



if __name__ == '__main__':
    create_dfs()

    cut_img_and_pdf_csv_path = "/home/jonasklotz/DSSGx/dssgx_land_sealing_dataset_analysis/data/labelled_data/parsed_pdfs_with_img_and_cut.csv"


    # read csv no header
    df = pd.read_csv(cut_img_and_pdf_csv_path, header=None)
    print(df.head())
    df.columns = ["path", "pdf_content", "img_content", "cut_img_content"]
    # replce newlines for all contents
    df["pdf_content"] = df["pdf_content"].apply(lambda x: x.replace("\n", ""))
    df["img_content"] = df["img_content"].apply(lambda x: x.replace("\n", ""))
    df["cut_img_content"] = df["cut_img_content"].apply(lambda x: x.replace("\n", ""))

    # calculate length for each content column
    df["pdf_content_len"] = df["pdf_content"].apply(lambda x: len(x))
    df["img_content_len"] = df["img_content"].apply(lambda x: len(x))
    df["cut_img_content_len"] = df["cut_img_content"].apply(lambda x: len(x))

    # get mean word count for each content column
    df["pdf_content_mean_word_count"] = df["pdf_content"].apply(lambda x: len(x.split(" ")))
    df["img_content_mean_word_count"] = df["img_content"].apply(lambda x: len(x.split(" ")))
    df["cut_img_content_mean_word_count"] = df["cut_img_content"].apply(lambda x: len(x.split(" ")))

    print(df.head())