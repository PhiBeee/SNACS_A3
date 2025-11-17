def get_hashtag_set(edges):
    '''
    Simple function to return a list of the set of hashtags
    '''
    hashtags = [edge[1] for edge in edges]
    return list(set(hashtags))

def get_user_set(edges):
    '''
    Simple function that returns a list of the set of users
    '''
    users = [edge[0] for edge in edges]
    return list(set(users))

def why_no_bipartite(edges):
    '''
    Function to figure out which hashtags are also users for some reason
    Will return which users are also in the hashtags for some fucking reason
    
    @param edges: Edge tuples as loaded by our function
    '''
    hashtags = get_hashtag_set(edges)
    users = list(set([edge[0] for edge in edges]))

    double_entries = []
    for user in users:
        if user in hashtags:
            double_entries.append(user)

    return double_entries

def edges_to_remove(overlap, edges):
    # Returns all edges where the user is in the overlap
    return [edge for edge in edges if edge[0] in overlap]

def from_graph_edges_to_our_format(g):
    '''
    Convenience function to turn networkx graph weighted edges into our own format

    @param g: networkx weighted graph
    :returns: List with (u, v, weight)
    '''
    edges = g.edges
    formatted_edges = []
    for edge in edges:
        edge_data = g.get_edge_data(edge[0], edge[1])
        formatted_edges.append((edge[0], edge[1], edge_data['weight']))
        
    return formatted_edges

def how_many_edges(overlap, edges):
    '''
    Function to see how many edges the users in the overlap account for
    Used for testing, prints to terminal

    @param overlap: List of users that overlap with hashtags
    @param edges: Full edge list
    '''
    for user in overlap:
        user_edges = [edge for edge in edges if user == edge[0]]
        print(f'{user}: {len(user_edges)}')

def remove_overlap(edges, graph):
    '''
    Convenience function to remove the users that are also hashtags

    @param edges: List of edge tuples
    @param graph: The networkx graph to be modified
    :returns: The new graph without overlap between hashtag and users as well as the new list of edges
    '''
    overlap = why_no_bipartite(edges)
    graph.remove_edges_from(edges_to_remove(overlap, edges))
    new_edges = from_graph_edges_to_our_format(graph)
    return graph, new_edges