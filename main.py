from preprocess import load, mention_graph

def main():
    data = load('small')
    mg = mention_graph(data)

if __name__ == '__main__':
    main()