import re
from tqdm import tqdm

def mention_graph(data, lenient = False, rt = True, subrt = False):
    '''
    Returns a dictionary with the node as the key and a list of mentions from which weight can be extrapolated

    @param data: list of lists as formatted by the load function
    @param lenient: boolean indicating whether we accept a whitespace between the @ or not
    @param rt: Whether to include retweet's in the graph too
    @param subrt: Whether to include mentions within a retweet or not
    :returns: dict(str:[str])
    '''
    mentions = dict()
    for tweet in tqdm(data):
        user = tweet[1]
        # Remove cut off mentions at the end of a tweet
        tweet[2] = re.sub(r'[@](\w{4,}|\s\w{4,})\s[.]{3,}', '')

        # If we don't accept retweets we just remove everything after the retweet from the string
        if not rt:
            tweet[2] = re.sub(r'[R][T]\s[@](\w{4,}|\s\w{4,}).*', '')
        elif not subrt:
            # Gets the position where the subtweet starts
            end_pos = re.search(r'[R][T]\s[@](\w{4,}|\s\w{4,})', tweet).span()[1]
            # Only keeps the quote tweet and the RT account
            tweet[2] = tweet[2][:end_pos]

        # allows for single space separation because twitter users sometimes dont want to notify the person
        if lenient: tweet_mentions = re.findall(r'[@](\w{4,}|\s\w{4,})', tweet[2])
        else: tweet_mentions = re.findall(r'[@]\w{4,}', tweet[2])

        # Clean up for processing
        tweet_mentions = [mention.replace('@', '') for mention in tweet_mentions]

        # Remove occurences of self mentioning and of fully numeric mentions in case those escape the 4 character min
        tweet_mentions = [mention for mention in tweet_mentions if mention != user and not mention.isnumeric()]

        # Add everything to our dict
        if user in mentions.keys():
            mentions[user] += tweet_mentions
        else: mentions[user] = tweet_mentions

    return mentions

def save_mentions_graph(graph: dict, data_size: str):
    '''
    Saves the mention graph to a file

    @param graph: Dictionnary containing as key the users and as value a list of users they mentioned
    @param data_size: string indicating which data set size is being processed
    '''
    out = []
    for user in graph.keys():
        for mention in set(graph[user]):
            # Add (user, mention, weight) to our list
            out.append(f'{user},{mention},{graph[user].count(mention)}')

    with open(f'mentions_{data_size}.csv', 'w+') as f:
        for item in out:
            f.write(f'{item}\n')
    f.close()