from load_data import load
from preprocess_mentions import mention_graph, save_mentions_graph

def main():
    data = load('small')
    mg = mention_graph(data)

if __name__ == '__main__':
    main()