import pandas as pd
import datetime
import math
import os

import lib.wordcloudcreator as wordcloudcreator
import lib.textminer as textminer
import lib.analysis as analysis


def extract_frontier(cleaned_df):
    number_of_cluster = int(cleaned_df["Cluster"].max() + 1)
    frontier_list = []
    for x in range(0, number_of_cluster):
        frontier_list.append([])
    for index, row in cleaned_df.iterrows():
        frontier_index = row["Cluster"]
        if (math.isnan(frontier_index)):
            frontier_index = int(number_of_cluster)
        #Title, Year, Keyword, TimesCited, TimesCiting -> to add Journal and Abstract
        publication = [row["Article Title"], row["Publication Year"], 
                        row["Abstract"], row["Keywords"], 
                        row["Cited Reference Count"], row["Times Cited, WoS Core"]]
        frontier_list[int(frontier_index - 1)].append(publication)
    
    return frontier_list

def create_individual_frontier_df(frontier_list, file_path):
    frontier_df_list = []
    frontier_linegraph_data = {}
    for frontier in frontier_list:
        current_frontier_df = pd.DataFrame(frontier, columns = ['Title', 'Year', 'Abstract', 'Keywords', 'Citing Others', 
        'Cited by Others'])
        frontier_words = textminer.mine_paper_info(current_frontier_df)
        frontier_name = textminer.mine_frontier_name(frontier_words)
        frontier_df_list.append((frontier_name, current_frontier_df))
        if not os.path.exists(file_path + frontier_name):
            os.makedirs(file_path + frontier_name)
        excel_path = file_path + "/{}/{}.xlsx".format(frontier_name, frontier_name)
        wordcloud_path = file_path + "/{}/wordcloud.png".format(frontier_name)
        linegraph_path = file_path + "/{}/linegraph.png".format(frontier_name)
        current_frontier_df.to_excel(excel_path, index=False)
        wordcloudcreator.generate_word_cloud(frontier_words, wordcloud_path)
        linegraph_data = wordcloudcreator.generate_year_linegraph(current_frontier_df, linegraph_path)
        frontier_linegraph_data[frontier_name] = linegraph_data

    return frontier_df_list, frontier_linegraph_data

def create_frontier_summary_df(frontier_df_list, linegraph_data, total_doc, max_year, min_year, file_path):
    frontier_summary = []
    count = 1
    year_range = max_year - min_year
    for frontier_tuple in frontier_df_list:
        current_frontier = []
        frontier_name = frontier_tuple[0]
        frontier_type = get_frontier_type(frontier_tuple[1], year_range)
        frontier_size = len(frontier_tuple[1].index)
        count = count + 1
        frontier_growth, frontier_impact = get_frontier_stats(frontier_tuple[1], total_doc, max_year, min_year)
        current_frontier = [frontier_name, frontier_type, frontier_size, 
                            frontier_growth, frontier_impact]
        frontier_summary.append(current_frontier)

    frontier_summary_df = pd.DataFrame(frontier_summary, columns=['Name', 'Type', 'Size', 
                    'Growth Index', 'Impact Index'])
    excel_path = file_path + "/Frontier_Summary.xlsx"
    graph_path = file_path + "/Frontier_Linegraph.png"
    frontier_summary_df.to_excel(excel_path, index=False)
    wordcloudcreator.generate_summary_linegraph(linegraph_data, graph_path)
    return frontier_summary_df 

def get_frontier_stats(frontier, total_doc, max_year, min_year):
    total_no_of_citation = frontier["Cited by Others"].sum()
    total_no_of_entries = len(frontier.index)
    growth = analysis.growth_index(frontier, total_doc, max_year, min_year)
    impact = analysis.impact_index(total_no_of_citation, total_no_of_entries)
    # sci_based = analysis.sci_based_index()
    return growth, impact

def get_frontier_type(frontier, year_range):
    recently_emerging_counter = 0
    persistent_emerging_counter = set()
    current_year = datetime.datetime.now().year
    for index, row in frontier.iterrows():
        published_year = row["Year"]
        persistent_emerging_counter.add(published_year)
        if (published_year >= current_year - 3):
            recently_emerging_counter = recently_emerging_counter + 1
    frontier_type = None
    if (len(frontier) < 0):
        frontier_type = "Outlier"
    else:
        if ((recently_emerging_counter/len(frontier) * 100) >= 80):
            frontier_type = "Recently Emerging Frontier"
        elif (len(persistent_emerging_counter) > (year_range/2)):
            frontier_type = "Persistently Emerging Frontier"
        else:
            frontier_type = "Neutral Frontier"
    
    return frontier_type