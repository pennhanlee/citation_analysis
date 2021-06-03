from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk import RegexpTokenizer
import pandas as pd
import numpy as np

def mine_paper_info(frontier):
    combined_words = []
    filtered_words = []
    frontier["Abstract"] = frontier["Abstract"].fillna("")
    tokenizer = RegexpTokenizer(r"\w+")
    for index, row in frontier.iterrows():
        title_words = tokenizer.tokenize(row["Title"].lower())
        key_words = row["Keywords"].lower().split("; ")
        abstract_words = tokenizer.tokenize(row["Abstract"].lower())
        combined_words = combined_words + title_words + abstract_words + key_words

    stop_words = set(stopwords.words('english'))
    for word in combined_words:
        if word not in stop_words and len(word) > 0:
            filtered_words.append(word)

    fdist = FreqDist(filtered_words)
    no_of_words = len(fdist)
    return no_of_words , fdist.most_common(no_of_words), fdist

def mine_frontier(df, word_bank, no_of_doc):
    doc_word_count, frontier_fdist, frontier_word_list = mine_paper_info(df)
    list_of_word_tuples = []
    for word in frontier_fdist:
        total_word_count = word_bank[word[0]]
        value = tf_idf(word[1], doc_word_count, total_word_count, no_of_doc)
        list_of_word_tuples.append((word[0], value))
    list_of_word_tuples.sort(key=lambda x:x[1])
    frontier_name = list_of_word_tuples[0][0] + " " + list_of_word_tuples[1][0]  #Top 2 words
    return frontier_word_list, frontier_name

def mine_word_bank(frontier_df_list):
    word_dictionary = {}
    for df in frontier_df_list:
        freq_dist = mine_paper_info(df)
        for word in freq_dist:
            word_dictionary[word[0]] += word[1]
    return word_dictionary

def term_freq(word_count, no_of_word):
    return word_count/no_of_word

def inv_doc_freq(word_count, no_of_doc):
    return np.log(no_of_doc/(word_count + 1))

def tf_idf(word_count, doc_word_count, total_word_count, no_of_doc):
    tf = term_freq(word_count, doc_word_count)
    idf = inv_doc_freq(total_word_count, no_of_doc)
    tf_idf = tf * idf
    return tf_idf