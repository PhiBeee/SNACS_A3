from convenience import get_user_set
import networkx as nx
from tqdm import tqdm

def project_weighted_edge_list(edges):
    '''
    Function that projects our graph by forming relations between two users who have used the same hashtag.
    The weight of the projected edge will be the 
    sum of all weights the user had to the hashtags in common with the other user.
    Saves the projection to a file as it goes along

    @param edges: List of edges (u,v,w) user, hashtag, weight
    '''
    users = get_user_set(edges)

    # Relational dictionnary for faster processing
    g = nx.DiGraph()
    g.add_weighted_edges_from(edges)

    # Get a reverse so we can lookup the hashtags faster 
    g_r = g.reverse(True)
    
    # Erase content from previous run 
    open('../data/hashtags_projected_small.csv', 'w', encoding='utf-8').close()

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
        # Save to file as we iterate through the users to avoid RAM overflow
        append_to_file(projection_format_to_file_format(([(user,relation_dict)])))    


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

def append_to_file(save_format):
    '''
    Takes the edges ready to be saved and appends them to the file
    This is to avoid RAM memory overflow by saving the edges as we project
    '''

    with open('../data/hashtags_projected_small.csv', 'a+', encoding='utf-8') as f:
        for entry in save_format:
            f.write(f'{entry[0]},{entry[1]},{entry[2]}\n')

    f.close()