import ast
import csv


def get_username_set(filename):
    """
    Get a set of usernames per file
    """
    with open(f"../data/{filename}_test__alt.csv",encoding="utf-8", newline="") as file:
        user_set = set()
        for line in file:
            if filename == "mentions":
                line = line.strip().split(',')
            else:
                line = line.strip().split(';')
            # Separate to make it more clear
            user = line[0]
            user_set.add(user)
    return user_set, len(user_set)

#not_correct
hashtag_username_set, length_hashtag_set = get_username_set("hashtags")
mentions_username_set, length_mentions_set = get_username_set("mentions")
topics_username_set, length_topics_set = get_username_set("topics")

final_set = hashtag_username_set.copy()
final_set.update(mentions_username_set)
final_set.update(topics_username_set)
total_users = len(final_set)
print(length_hashtag_set, length_mentions_set, length_topics_set, total_users)

def get_total(filename):
        """ 

        """
        count = 0
        with open(f"../data/{filename}_test__alt.csv",encoding="utf-8", newline="") as file:
            for line in file:
                line = line.strip().split(';')
                weights = ast.literal_eval(line[-1])
                count += sum(weights)
        return count


hashtag_total = get_total("hashtags")
mentions_total = len(mentions_username_set)
topics_total = get_total("topics")

print(hashtag_total, "hashtag total")
print(mentions_total, "mentions total")
print(topics_total, "topics total")

def find_u2u(filename,username):
    with open(f"../data/{filename}_test__alt.csv",encoding="utf-8", newline="") as file:

        #will not be used for hashtags
        to_users = [] 
        weights = []
        for line in file:
            if filename == "mentions":
                line = line.strip().split(',')
                user = line[0]
                if user == username:
                    to_users.append(line[1])
                    weights.append(int(line[-1]))
                
                
            else:
                line = line.strip().split(';')
                user = str(line[0])
                if user == username:
                    return ast.literal_eval(line[1]),ast.literal_eval(line[-1]) 
                    break
        #will only be used in case of the mentions file, return the lists
    if filename == "mentions":
        print(to_users, len(to_users),type(to_users))
        print(weights, len(weights),type(weights))

    return to_users,weights 
            
            
for user in final_set:
    calculated = {}

    if user in hashtag_username_set:
        u2u,weights_u2u = find_u2u("hashtags",user)
        for count in range(len(u2u)):
            hashtag_intermediate = (total_users*weights_u2u[count])/hashtag_total
            calculated[(user,u2u[count])]=[hashtag_intermediate,0,0]
        
    if user in topics_username_set:
        u2u,weights_u2u = find_u2u("topics",user)
        for count in range(len(u2u)):
            topics_intermediate = (total_users*weights_u2u[count])/topics_total
            if (user,u2u[count]) in calculated:
                calculated[(user,u2u[count])][1] = topics_intermediate
            else:
                calculated[(user,u2u[count])]=[0,topics_intermediate,0]
            
    if user in mentions_username_set:
        u2u,weights_u2u = find_u2u("mentions",user)
        for count in range(len(u2u)):
            mentions_intermediate = (total_users*weights_u2u[count])/mentions_total
            if (user,u2u[count]) in calculated:
                calculated[(user,u2u[count])][2] = mentions_intermediate
            else:
                calculated[(user,u2u[count])]=[0,0,mentions_intermediate]
                
    with open("output.csv", "a",encoding="utf-8",newline="") as final_weights:
        writer = csv.writer(final_weights)
        for key, value in calculated.items():
            username = str(key[0])
            username_in = str(key[1])
            weight_u1_u2 = sum(value)
            writer.writerow([username, username_in, weight_u1_u2])
