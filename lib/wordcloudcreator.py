from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

def plot_cloud(wordcloud):
    plt.figure(figsize=(40, 30))
    plt.imshow(wordcloud)
    plt.axis("off")
    return None


def generate_word_cloud(list_of_words, save_path):
    wordcloud = WordCloud(width = 3000, height = 2000, random_state=1,
                background_color='grey', colormap='Pastel1', collocations=False,
                stopwords = STOPWORDS).generate(" ".join(list_of_words))

    # plot_cloud(wordcloud)
    wordcloud.to_file(save_path)
    return None


def generate_year_linegraph(frontier, save_path):
    frontier = frontier["Year"].value_counts().sort_index(ascending=True)
    for x in range(1, len(frontier.values)):
        frontier.values[x] = frontier.values[x] + frontier.values[x-1]

    plt.plot(frontier.index, frontier.values, color="red", marker="o")
    plt.xlabel("Years")
    plt.ylabel("Culmulative Papers Published")
    plt.grid(True)
    plt.savefig(save_path)
    plt.close()
    return (frontier.index, frontier.values)

def generate_summary_linegraph(linegraph_data, save_path):
    for key in linegraph_data.keys():
        print(key)
        plt.plot(linegraph_data[key][0], linegraph_data[key][1], label=key)
    plt.xlabel("Years")
    plt.ylabel("Culmulative Papers Published")
    plt.grid(True)
    lg = plt.legend(bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.savefig(save_path,
                format='png', 
                bbox_extra_artists=(lg,), 
                bbox_inches='tight')
    plt.close()
    return None