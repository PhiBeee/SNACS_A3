def load(file: str) -> list:
    '''
    Function to load the .tsv datasets as a list of lists
    Each list in the list contains one entry

    @param file: string denoting which size file to load
    :return: A list of lists with each list's elements being one column
    '''
    filename = 'twitter-'+file+'.tsv'
    data = []
    with open(filename) as file:
        data = [line.strip().split('\t') for line in file]

    return data