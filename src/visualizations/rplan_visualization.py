import os

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from utility.config_utils import get_data_path

data_path = get_data_path()


def plot_keyword_search_results(result_df, keyword_columns: list, title: str = "Keyword Search Results"):
    """ Function to plot the results of a keyword search

    Args:
        result_df: Result df of the keyword search
        keyword_columns: List of columns containing the keywords
        title: Title of the plot

        """

    keyword_counts = result_df[keyword_columns].apply(pd.Series.value_counts)
    # remove the False row
    keyword_counts = keyword_counts.drop([False])
    keyword_counts = keyword_counts.transpose()
    # plot with seaborn
    sns.set(style="whitegrid")  # Optional: Set a white grid background

    plt.figure(figsize=(15, 5))

    fig2 = sns.barplot(x=keyword_counts.index, y=keyword_counts[True], palette="Set2")
    # align the filenames diagonal and rotate them
    fig2.set_xticklabels(fig2.get_xticklabels(), rotation=45, horizontalalignment='right')
    # set the value of each bar
    for p in fig2.patches:
        fig2.annotate(format(p.get_height(), '.0f'),
                      (p.get_x() + p.get_width() / 2., p.get_height()),
                      ha='center',
                      va='center',
                      xytext=(0, 10),
                      textcoords='offset points')

    fig2.set_title(title)
    plt.tight_layout()
    fig2.set_xlabel("Keyword")
    fig2.set_ylabel("Count of Occurrences")
    plt.show()


def visualize_sections(input_df: 'pd.DataFrame'):
    """ Function to visualize the section types per region

    Args:
        input_df: Input df to be visualized

        """
    # remove all start sections
    input_df = input_df[input_df["section_type"] != "start"]
    # remove all that dont have a name
    input_df = input_df[input_df["Name"] != ""]

    # plot a bar plot of the section types per filename
    sns.set(style="whitegrid")  # Optional: Set a white grid background

    plt.figure(figsize=(15, 5))  # Adjust the figure size to control width and height

    # Create the bar plot using Seaborn
    # for each filename create 3 bars for the 3 section types displaying the count of each section type
    fig2 = sns.countplot(x="Name", hue="section_type", data=input_df, palette="Set2")
    # align the filenames diagonal and rotate them
    fig2.set_xticklabels(fig2.get_xticklabels(), rotation=45, horizontalalignment='right')
    # allocate more space for the labels
    plt.tight_layout()

    fig2.set_xlabel("Regionname")
    fig2.set_ylabel("Count of sections")
    fig2.set_title("Section types per region")
    plt.show()