def load(file: str) -> list:
    '''
    Function to load the .tsv datasets as a list of lists
    Each list in the list contains one entry

    @param file: string denoting which size file to load
    :return: A list of lists with each list's elements being one column
    '''
    filename = '../data/twitter-'+file+'.tsv'
    data = []
    with open(filename) as file:
        data = [line.strip().split('\t') for line in file]

    return data

def load_processed_graph(name: str, data_size: str):
    '''
    Function to load in the .csv files of our graphs after they have been processed

    @param name: Name of the graph to load
    :returns: List as loaded from the file as tuples (u, v, w)
    '''
    filename = '../data/'+name+'_'+data_size+'.csv'
    data = []
    # Read in our lines
    with open(filename)as file:
        data = [line.strip().split(',') for line in file]

    # Turn them into tuples (from, to, weight)
    data = [(line[0], line[1], int(line[2])) for line in data]

    return data