from load_data import load, load_processed_graph
from preprocess_mentions import mention_graph, save_mentions_graph
from preprocess_hashtags import hashtag_graph, save_bipartite_hashtag_graph, project_graph

def generate_data_files(data_size: str, lenient = True, rt = True, subrt = True):
    '''
    This is the function that will generate all the preprocessed edge weight files for all the graphs.
    All the edge weights files will be saved under the data directory and can be loaded in with the function for it.

    @param data_size: The data size of the initial twitter file
    @param lenient: Whether to be lenient with the mention graph or not, allowing a whitespace between the @ and the usenrname
    @parma rt: Flag to include or exclude rt mention and content
    @param subrt: Flag to ignore only content within the retweet but accept person being retweeted
    '''
    data = load(data_size)
    mg = mention_graph(data, lenient = lenient, rt = rt, subrt = subrt)
    save_mentions_graph(mg, data_size)

    hg = hashtag_graph(data, rt = rt)
    save_bipartite_hashtag_graph(hg, data_size)

    ht_edges = load_processed_graph('hashtags_bipartite', data_size)
    project_graph(ht_edges)