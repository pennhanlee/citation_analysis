import pandas as pd
import sys
import os
import datetime
import time
import math

import lib.pdfscrap as pdfscrap
import lib.analysis as analysis

#Temporary URl Hardcode
CLUSTER_FILEPATH = "./data/cluster/vosviewer_graph_1_500.csv"
FULLRECORD_FILEPATH = "./data/cluster/computervision_fullrec_nocr.xls"
JOURNAL_FILEPATH = "./data/cluster/CiteScore_2011_2019.xlsb"
JOURNAL_SHEETNAME = "CiteScore 2019"
MAX_YEAR = 2021
YEAR_RANGE = 10


def pdf_scrap_handler():
    pdfscrap.citationExtractor()

def heat_map_handler():
    print("Feature Coming Soon")

def error(user_input):
    print("Did not understand your input: " + user_input)
    return None


def pdf_extraction():
    try:
        while True:
            print("Citation Analysis Programme \nPress 'Ctrl C' to quit this program \n")
            user_input = input("Please select an option: \n1. Load new PDF file \n2. Generate Heat Map \n")
            if user_input == "1":
                pdf_scrap_handler()
            elif user_input == "2":
                heat_map_handler()
            else:
                error(user_input)

    except KeyboardInterrupt:
        print("Terminating Citation Analysis Programme")
        time.sleep(2)
        pass
    
    return None

def prepare_fullrecord_df(fullrecord_df, cluster_df, journal_df):
    df = fullrecord_df

    df["Keywords"] = df[['Author Keywords' , 'Keywords Plus']].fillna('').apply("; ".join, axis = 1)

    df = df.drop(columns=["Book Authors", "Book Editors", "Book Group Authors", 
                            "Book Author Full Names", "Group Authors", 
                            "Author Keywords", "Keywords Plus",
                            "Book Series Title", "Book Series Subtitle", "Language", 
                            "Conference Title", "Conference Date", "Conference Location", 
                            "Conference Sponsor", "Conference Host", "Addresses", "Reprint Addresses",
                            "Email Addresses", "Researcher Ids", "ORCIDs",
                            "Funding Orgs", "Funding Text", "Cited References",
                            "Publisher", "Publisher City", "Publisher Address", "Publication Date",
                            "Part Number", "Supplement", "Special Issue", "Meeting Abstract",
                            "Article Number", "Book DOI", "Early Access Date", "Number of Pages",
                            "Open Access Designations", "Highly Cited Status", "Hot Paper Status",
                            "Date of Export", "Unnamed: 67"], axis=1)

    df['ISSN'] = df["ISSN"].replace("-", "", regex=True)
    df['eISSN'] = df["eISSN"].replace("-", "", regex=True)


    # for index, row in df.iterrows():
    #     journal_issn = row["ISSN"]
    #     journal_eissn = row["eISSN"]
    #     df = pd.merge(df, journal_df[["CiteScore", "SNIP", "SJR"]], how="left", left_on = ["ISSN"], right_on = ["Print ISSN"])

    df["Cluster"] = cluster_df["cluster"]
    df["Normalised Bib Coupling Weight"] = cluster_df["weight<Norm. citations>"]
    # print(df)
    return df

def get_frontier_type(frontier):
    recently_emerging_counter = 0
    persistent_emerging_counter = set()
    current_year = datetime.datetime.now().year
    for index, row in frontier.iterrows():
        published_year = row["Year"]
        persistent_emerging_counter.add(published_year)
        if (published_year >= current_year - 3):
            recently_emerging_counter = recently_emerging_counter + 1
    frontier_type = None
    if ((recently_emerging_counter/len(frontier) * 100) >= 80):
        frontier_type = "Recently Emerging Frontier"
    elif (len(persistent_emerging_counter) > (YEAR_RANGE/2)):  #Currently hardcoded for 10 years
        frontier_type = "Persistently Emerging Frontier"
    else:
        frontier_type = "Neutral Frontier"
    
    return frontier_type

def get_frontier_stats(frontier, total_doc, max_year, min_year):
    total_no_of_citation = frontier["Cited by Others"].sum()
    total_no_of_entries = len(frontier.index)
    growth = analysis.growth_index(frontier, total_doc, max_year, min_year)
    impact = analysis.impact_index(total_no_of_citation, total_no_of_entries)
    # sci_based = analysis.sci_based_index()
    return growth, impact

def get_frontier_name(frontier):
    return None

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
                        row["Keywords"], row["Cited Reference Count"], 
                        row["Times Cited, WoS Core"]]
        frontier_list[int(frontier_index - 1)].append(publication)
    
    return frontier_list


def create_individual_frontier_df(frontier_list):
    frontier_count = 1
    current_time = "today"
    frontier_df_list = []
    if not os.path.exists("./data/cluster/" + str(current_time)):
            os.makedirs("./data/cluster/" + str(current_time))
    for frontier in frontier_list:
        current_frontier_df = pd.DataFrame(frontier, columns = ['Title', 'Year', 'Keywords', 'Citing Others', 
        'Cited by Others'])
        frontier_df_list.append(current_frontier_df)
        path = "./data/cluster/{}/{}.xlsx".format(current_time ,frontier_count)
        current_frontier_df.to_excel(path, index=False)
        frontier_count = frontier_count + 1

    return frontier_df_list

def create_frontier_summary_df(frontier_df_list, total_doc, max_year, min_year):
    frontier_summary = []
    count = 1
    for frontier in frontier_df_list:
        current_frontier = []
        frontier_name = get_frontier_name(frontier)
        frontier_type = get_frontier_type(frontier)
        frontier_size = len(frontier.index)
        print("NEXT FRONTIER: " + str(count))
        count = count + 1
        frontier_growth, frontier_impact = get_frontier_stats(frontier, total_doc, max_year, min_year)
        print("\nFrontier Growth: " + str(frontier_growth))
        print("Frontier Impact: " + str(frontier_impact) + "\n")
        current_frontier = [frontier_name, frontier_type, frontier_size, 
                            frontier_growth, frontier_impact]
        frontier_summary.append(current_frontier)

    frontier_summary_df = pd.DataFrame(frontier_summary, columns=['Name', 'Type', 'Size', 
                    'Growth Index', 'Impact Index'])

    return frontier_summary_df 

def main():
    # cluster_path = input("Please provide cluster csv filepath \n")
    fullrecord_path = input("Please provide fullrecord excel filepath \n")
    cluster_df = pd.read_csv(CLUSTER_FILEPATH)
    fullrecord_df = pd.read_excel(FULLRECORD_FILEPATH)
    #journal_df = pd.read_excel(JOURNAL_FILEPATH, sheet_name=JOURNAL_SHEETNAME, engine='pyxlsb')
    journal_df = pd.read_excel(FULLRECORD_FILEPATH) #Temporary, the loading of journal takes too long for testing
    cleaned_fullrecord_df = prepare_fullrecord_df(fullrecord_df, cluster_df, journal_df)
    cleaned_fullrecord_df.to_excel("./data/cluster/cleaned.xlsx", index=False)
    max_year = MAX_YEAR
    min_year = max_year - YEAR_RANGE
    total_doc = len(cleaned_fullrecord_df.index)
    frontier_list = extract_frontier(cleaned_fullrecord_df)
    frontier_df_list = create_individual_frontier_df(frontier_list)
    frontier_summary_df = create_frontier_summary_df(frontier_df_list, total_doc, max_year, min_year)
    return None


if __name__ == "__main__":
    try:
        print("Citation Analysis Programme \nPress 'Ctrl C' to quit this programme")
        while True:
            main()

    except KeyboardInterrupt:
        print("Terminating Citation Analysis Programme")
        pass
