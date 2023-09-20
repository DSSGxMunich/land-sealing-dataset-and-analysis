import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from utility.config_utils import get_data_path, get_source_path



data_path = get_data_path()
content_path = os.path.join(data_path, "nrw", "extracted_rplan_content.json")

def plot_keyword_search_results(result_df, keyword_columns:list, title:str="Keyword Search Results"):
    # plot the number of true values in each keyword column
    # for each keyword column count the number of true values
    # create a new df with the counts
    keyword_counts = result_df[keyword_columns].apply(pd.Series.value_counts)
    # remove the False row
    keyword_counts = keyword_counts.drop([False])
    # transpose the df
    keyword_counts = keyword_counts.transpose()
    # plot with seaborn
    sns.set(style="whitegrid")  # Optional: Set a white grid background

    plt.figure(figsize=(15, 5))  # Adjust the figure size to control width and height

    # Create the bar plot using Seaborn
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

    # set title
    fig2.set_title(title)
    # allocate more space for the labels
    plt.tight_layout()
    # set labels
    fig2.set_xlabel("Keyword")
    fig2.set_ylabel("Count of Occurrences")
    plt.show()



def visualize_sections(input_df):
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
    #plt.savefig("section_type.png")

if __name__ == '__main__':
    input_df = pd.read_json(content_path)
    visualize_sections(input_df)
