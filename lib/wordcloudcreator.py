from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

def plot_cloud(wordcloud):
    plt.figure(figsize=(40, 30))
    plt.imshow(wordcloud)
    plt.axis("off")


def generate_word_cloud(list_of_words, save_path):
    wordcloud = WordCloud(width = 3000, height = 2000, random_state=1,
                background_color='grey', colormap='Pastel1', collocations=False,
                stopwords = STOPWORDS).generate(" ".join(list_of_words))

    # plot_cloud(wordcloud)
    wordcloud.to_file(save_path)