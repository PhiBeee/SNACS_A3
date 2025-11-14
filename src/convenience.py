def get_hashtag_set(edges):
    '''
    Simple function to return a list of the set of hashtags
    '''
    hashtags = [edge[1] for edge in edges]
    return list(set(hashtags))

def why_no_bipartite(edges):
    '''
    Function to figure out which hashtags are also users for some reason
    Will print to terminal which users are also in the hashtags for some fucking reason
    
    @param edges: Edge tuples as loaded by our function
    '''
    hashtags = get_hashtag_set(edges)
    users = list(set([edge[0] for edge in edges]))

    for user in users:
        if user in hashtags:
            print(f'Evil fucking bastard: {user}')

    # TODO: Figure out what to do with these overlaps