from nltk import word_tokenize
from nltk.probability import FreqDist
from nltk.corpus import stopwords
from nltk import RegexpTokenizer

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
    return fdist

def mine_frontier_name(word_frequency):
    top_two_words = word_frequency.most_common(2)
    frontier_name = " ".join([x[0] for x in top_two_words])
    return frontier_name