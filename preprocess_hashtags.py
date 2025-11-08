import re 
import tqdm as tqdm

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
        tweet[2] = re.sub(r'[#]\w+\s[.]{3,}', '')

        # If we don't accept retweets we just remove everything after the retweet from the string
        if not rt:
            tweet[2] = re.sub(r'[R][T]\s[@](\w{4,}|\s\w{4,}).*', '')
        
        tweet_hashtags = re.findall(r'[#]\w+', tweet[2])

        # Clean up for processing
        tweet_hashtags = [hashtag.replace('#', '') for hashtag in tweet_hashtags]

        # Remove purely numeric hashtags
        tweet_hashtags = [hashtag for hashtag in tweet_hashtags if not hashtag.isnumeric()]

        # Add everything to our dict
        if user in hashtags.keys():
            hashtags[user] += tweet_hashtags
        else: hashtags[user] = tweet_hashtags

    return hashtags

def save_hashtag_graph(graph: dict, data_size: str):
    '''
    Saves the hashtag graph to a file
    Every line is structured as follows: user, hashtag, weight

    @param graph: Dictionnary with as key the user and as value a list of hashtags
    @param data_size: The size of the dataset we are saving
    '''

    out = []
    for user in graph.keys():
        for hashtag in set(graph[user]):
            out.append(f'{user},{hashtag},{graph[user].count(hashtag)}')

    with open(f'hashtags_{data_size}.csv', 'w+') as f:
        for item in out:
            f.write(f'{item}\n')

    f.close()