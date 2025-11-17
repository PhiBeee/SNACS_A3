from convenience import get_user_set
import networkx as nx
from tqdm import tqdm

# Slow and can lead to using too much memory
def project_weighted_edge_list(edges):
    '''
    Function that projects our graph by forming relations between two users who have used the same hashtag.
    The weight of the projected edge will be the 
    sum of all weights the user had to the hashtags in common with the other user.

    @param edges: List of edges (u,v,w) user, hashtag, weight
    :returns: Weird fucking format idk why I decided on this tbh
    '''
    users = get_user_set(edges)

    # Relational dictionnary for faster processing
    g = nx.DiGraph()
    g.add_weighted_edges_from(edges)

    # Get a reverse so we can lookup the hashtags faster 
    g_r = g.reverse(True)

    projected_edges = []
    for user in tqdm(users):
        relation_dict = {}
        # print(g[user])
        for hashtag in g[user].keys():
            # {user: {'weight': int}}
            related_users_dict = g_r[hashtag]
            related_users = list(related_users_dict.keys())
            for related_user in related_users:
                if related_user == user: continue
                # If user is already in the relation dict we add the weight
                if related_user in relation_dict.keys():
                    relation_dict[related_user] += g[user][hashtag]['weight']
                # If the user isnt in the relations dict we add the new entry
                else:
                    relation_dict[related_user] = g[user][hashtag]['weight']

        projected_edges.append((user,relation_dict))     

    return projected_edges  

def projection_2(edges):
    g = nx.DiGraph()
    g.add_weighted_edges_from(edges)

    pred = g.pred
    
    nodes = get_user_set(edges)

def projection_format_to_file_format(projected_edges):
    '''
    Takes the weird format from the projection and turns it into the proper format
    '''
    save_format = []
    for user in projected_edges:
        user_from = user[0]
        for user_to in user[1].keys():
            save_format.append((user_from, user_to, user[1][user_to])) # Wtf was I cooking

    return save_format