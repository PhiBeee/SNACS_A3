def load(file: str) -> list:
    '''
    Function to load the .tsv datasets as a list of lists
    Each list in the list contains one entry

    @param file: string denoting which size file to load
    :return: A list of lists with each list's elements being one column
    '''
    filename = '../data/twitter-'+file+'.tsv'
    data = []
    with open(filename,encoding="utf-8") as file:
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
    with open(filename,encoding="utf-8") as file:
        data = [line.strip().split(',') for line in file]

    # Turn them into tuples (from, to, weight)
    data = [(line[0], line[1], int(line[2])) for line in data]

    return data

def load_subset(name: str, data_size: str, amount_of_users: int):
    '''
    Function to load a subset of the dataset specified by the amount of users from which edges are going out

    @param name: name of the dataset file to subset, needs to have been preprocessed
    @param data_size: data_size of that dataset
    @param amount_of_users: the amount of users to take for the subset
    :returns: List of outgoing edges from the users of the selected subset
    '''
    # Set of users to keep track of unique users
    user_set = set({})
    edges = []

    filename = f'../data/{name}_{data_size}.csv'

    current_user = None
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip().split(',')
            # User change, since each user comes one after the other
            if line[0] != current_user:
                # Stop if we have the amount of users we wanted
                if len(user_set) == amount_of_users:
                    break

                user_set.add(line[0])
                current_user = line[0]
        
            edges.append((line[0], line[1], int(line[2])))

    return edges

def load_subset_alt(name: str, data_size: str, amount_of_users: int):
    '''
    Function to load in a subset of users from a file formatted using the alternative format

    @param name: name of the dataset to get a subset from, needs to be in alt format
    @param data_size: size of the dataset,
    @param amount_of_users: the amount of users to take for the subset from which there are outgoing edges
    :returns: List of outgoing edges from users of the subset
    '''
    edges = []

    filename = f'../data/{name}_{data_size}_alt.csv'

    flag = False
    users = 0
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            if not flag:
                print(line)
                flag = True
            line = line.strip().split(';')

            # Separate to make it more clear
            user = line[0]
            users_to = line[1][2:-2].split("', '") 
            weights = line[2][1:-1].split(',')

            for user_to, weight in zip(users_to, weights):
                edges.append((user, user_to, int(weight)))

            users += 1

            if users == amount_of_users:
                break

    return edges



