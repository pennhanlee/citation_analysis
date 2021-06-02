import pandas as pd
import sys
import os
import datetime
import time
import math
import shutil

import lib.pdfscrap as pdfscrap
import lib.analysis as analysis
import lib.textminer as textminer
import lib.wordcloudcreator as wordcloudcreator
import lib.researchfrontier as researchfrontier

#Temporary URl Hardcode
CLUSTER_FILEPATH = "./data/cluster/vosviewer_graph_1_500.csv"
FULLRECORD_FILEPATH = "./data/cluster/computervision_fullrec_nocr.xls"
JOURNAL_FILEPATH = "./data/cluster/CiteScore_2011_2019.xlsb"
JOURNAL_SHEETNAME = "CiteScore 2019"
MAX_YEAR = 2021
YEAR_RANGE = 10
CURRENT_TIME_STRING = ""

def pdf_scrap_handler():
    pdfscrap.citationExtractor()

def error(user_input):
    print("Did not understand your input: " + user_input)
    return None

def pdf_extraction():
    pdf_scrap_handler()
    return None

def prepare_fullrecord_df(fullrecord_df, cluster_df):
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

    # issn_version = journal_df.dropna(subset=['Print ISSN']).drop_duplicates(subset=["Scopus Source ID"])
    # print(issn_version.columns)
    # df = df.merge(issn_version[["CiteScore", "Print ISSN"]], how="left", left_on = ["ISSN"], right_on = ["Print ISSN"])

    df["Cluster"] = cluster_df["cluster"]
    df["Normalised Bib Coupling Weight"] = cluster_df["weight<Norm. citations>"]
    # print(df)
    return df

def main():
    # cluster_path = input("Please provide cluster csv filepath \n")
    # fullrecord_path = input("Please provide fullrecord excel filepath \n")
    # max_year = int(input("Please give the latest year for analysis Eg. 2021 \n"))
    # min_year = int(input("Please give the earliest year for analysis Eg. 2010 \n"))
    '''
    HARDCODE AREA FOR EASE OF CODING
    '''
    cluster_path = CLUSTER_FILEPATH
    fullrecord_path = FULLRECORD_FILEPATH
    max_year = MAX_YEAR
    min_year = MAX_YEAR - YEAR_RANGE
    print("Preparing provided data")
    cluster_df = pd.read_csv(cluster_path)
    fullrecord_df = pd.read_excel(fullrecord_path)
    # journal_df = pd.read_excel(JOURNAL_FILEPATH, sheet_name=JOURNAL_SHEETNAME, engine='pyxlsb')
    # journal_df = pd.read_excel(FULLRECORD_FILEPATH) # Temporary, the loading of journal takes too long for testing
    savefile_path = "./data/cluster/" + CURRENT_TIME_STRING + "/"
    cleaned_fullrecord_df = prepare_fullrecord_df(fullrecord_df, cluster_df)
    # cleaned_fullrecord_df.to_excel("./data/cluster/cleaned.xlsx", index=False)
    total_doc = len(cleaned_fullrecord_df.index)
    frontier_list = researchfrontier.extract_frontier(cleaned_fullrecord_df)
    frontier_df_list, accumulated_linegraph_data = researchfrontier.create_individual_frontier_df(frontier_list, 
                                                                                                    savefile_path)
    frontier_summary_df = researchfrontier.create_frontier_summary_df(frontier_df_list, 
                                                                        accumulated_linegraph_data, 
                                                                        total_doc, 
                                                                        max_year, min_year, 
                                                                        savefile_path)
    return None


if __name__ == "__main__":
    CURRENT_TIME_STRING = datetime.datetime.now().strftime("%d-%m-%Y_%H%M")
    try:
        print("Citation Analysis Programme \nPress 'Ctrl C' to quit this programme")
        main()
        print("Extracting of data for Citation Analysis complete")
    except Exception as e:
        print("An error occurred: " + e)
        mydir = "./data/cluster/{}".format(CURRENT_TIME_STRING)
        try:
            shutil.rmtree(mydir)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
        pass
