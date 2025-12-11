from preprocess_all import generate_data_files
from weight_calculation import calculate_weights_main

def main():
    data_size = 'small'

    # Initial generation of the graphs
    # generate_data_files(
    #     data_size = data_size,
    #     lenient = True,
    #     rt = True,
    #     subrt = False 
    # )

    calculate_weights_main(
        old_method = False,
        new_method = True,
    )



if __name__ == '__main__':
    main()