import re
from tqdm import tqdm
# used this data to test -> this is also a good example tweet with multiple retweets, maybe take only the first retweet? I am not sure how it works
# data = [["khopkinson","RT @changeisgood1: RT @Java4Two: RT @MsFitUniverse: #FollowFriday @JimWray @WholeFoods @BrennanAnnie @WannabeSkinny @slkeeth @lalalalu"]]
def retweet_graph(data):
    '''
    Returns a dictionary with the node as the key and a list of mentions from which weight can be extrapolated

    @param data: list of lists as formatted by the load function
    @param lenient: boolean indicating whether we accept a whitespace between the @ or not
    @param rt: Whether to include retweet's in the graph too. 
    This is set to False because the old paper which we are comparing with has a separate weight element for this
    @param subrt: Whether to include mentions within a retweet or not
    This is set to False because the old paper which we are comparing with has a separate weight element for this

    :returns: dict(str:[str])
    '''
    print("Making retweet graph")
    rts = dict()
    for tweet in tqdm(data):
        user = tweet[1]
        # Remove cut off mentions at the end of a tweet
        tweet[2] = re.sub(r'[@](\w{4,}|\s\w{4,})\s[.]{3,}', '', tweet[2])

        # Find all retweets in the string, retweets are RT @alice_: they always have a : and a RT. 
        #Note that you don't want the mentions in the retweets, only to which username the user is retweeting. 
        all_rts = re.findall(r'RT\s*@(\w+):', tweet[2])

        # Remove occurences of self mentioning and of fully numeric mentions in case those escape the 4 character min
        tweet_retweets = [retweet for retweet in all_rts if retweet != user and not retweet.isnumeric()]

        # Add everything to our dict
        if user in rts.keys():
            rts[user] += tweet_retweets
        else: rts[user] = tweet_retweets

    return rts

def save_retweet_graph(graph: dict, data_size: str):
    '''
    Saves the retweet graph to a file

    @param graph: Dictionnary containing as key the users and as value a list of users they mentioned
    @param data_size: string indicating which data set size is being processed
    '''
    print("Saving retweet file")
    out = []
    for user in graph.keys():
        for retweet in set(graph[user]):
            # Add (user, mention, weight) to our list
            out.append(f'{user},{retweet},{graph[user].count(retweet)}')

    with open(f'../data/retweets_{data_size}.csv', 'w+', encoding='utf-8') as f:
        for item in out:
            f.write(f'{item}\n')
    f.close()