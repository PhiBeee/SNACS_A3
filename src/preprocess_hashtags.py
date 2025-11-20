import re 
import networkx as nx

from tqdm import tqdm
from convenience import remove_overlap
from projection import project_weighted_edge_list

def hashtag_graph(data, rt = True):
    '''
    Generates the hashtag graph for each user.

    @param data: The data as parsed by the load function
    @param rt: Flag indicating whether we accept the contents of a rt or not
    :returns: A dictionary with as key the user and as value a list of hashtags they have used
    '''

    hashtags = dict()
    for tweet in tqdm(data):
        user = tweet[1]

        # Remove cut off hashtags at the end of a tweet
        tweet[2] = re.sub(r'[#]\w+\s[.]{3,}', '', tweet[2])

        # If we don't accept retweets we just remove everything after the retweet from the string
        if not rt:
            tweet[2] = re.sub(r'[R][T]\s[@](\w{4,}|\s\w{4,}).*', '', tweet[2])
        
        tweet_hashtags = re.findall(r'[#]\w+', tweet[2])

        # Clean up for processing
        tweet_hashtags = [hashtag.replace('#', '') for hashtag in tweet_hashtags]

        # Remove purely numeric hashtags and lowercase hashtags
        tweet_hashtags = [hashtag.lower() for hashtag in tweet_hashtags if not hashtag.isnumeric()]

        # Add everything to our dict
        if user in hashtags.keys():
            hashtags[user] += tweet_hashtags
        else: hashtags[user] = tweet_hashtags

    return hashtags

def project_graph_and_save(edges: list, remove_overlap_flag: bool, data_size: str):
    '''
    This function takes the hashtag graph, which should be bipartite and projects it 
    so we have the connection between the users based on their hashtag usage
    After projecting saves it to a file.

    @param edges: Our bipartite graph as a list of tuples (from, to, weight)
    @param remove_overlap_flag: Boolean to decide whether to remove user/hashtag overlap or not
    :returns: The projection of that graph
    '''
    # Grabs our edges and turns them into a nx graph, only really needed to remove the overlap
    g = nx.DiGraph()
    g.add_weighted_edges_from(edges)
    if remove_overlap_flag: g, edges = remove_overlap(edges, g)
    # The networkx function was too weird so I made my own
    project_weighted_edge_list(edges)

def save_bipartite_hashtag_graph(graph: dict, data_size: str):
    '''
    Saves the hashtag graph to a file
    Every line is structured as follows: user, user, weight

    @param graph: Dictionnary with as key the user and as value a list of hashtags
    @param data_size: The size of the dataset we are saving
    '''

    out = []
    for user in graph.keys():
        for hashtag in set(graph[user]):
            out.append(f'{user},{hashtag},{graph[user].count(hashtag)}')

    with open(f'../data/hashtags_bipartite_{data_size}.csv', 'w+',encoding="utf-8") as f:
        for item in out:
            f.write(f'{item}\n')

    f.close()