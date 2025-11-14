from preprocess_all import generate_data_files

def main():
    data_size = 'small'

    # Initial generation of the graphs
    generate_data_files(
        data_size = data_size,
        lenient = True,
        rt = True,
        subrt = False 
    )


if __name__ == '__main__':
    main()