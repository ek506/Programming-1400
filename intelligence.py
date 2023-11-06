from matplotlib import pyplot as plt
import numpy as np
import utils


def find_red_pixels(map_filename="./data/map.png", upper_threshold=100, lower_threshold=50):
    """
Takes an image as an input and finds all the red pixels in that image and marks their location in a 2D
numpy array red_array. red_array is written as a black and white image to map-red-pixels.jpg where red pixels
are represented by white and non-red pixels are represented by black

     Args:
         map_filename: file location of the image used
         upper_threshold: Minimum amount of red needed in a pixel to mark it as red
         lower_threshold: Maximum amount of blue or green allowed in a pixel to still mark it as red

     Returns:
         red_array: 2D numpy array of 0's for red pixels and 1's for non-red pixels
     """

    rgb_img = plt.imread(map_filename)  # creates 3D numpy array of image
    height, width = rgb_img.shape[0], rgb_img.shape[1]
    red_array = np.array([[1] * width for _ in range(height)])  # list of 1's used as black image

    for row_index, row in enumerate(rgb_img):
        for col_index, col in enumerate(row):
            pixel = rgb_img[row_index][col_index]*255  # multiply up rgb values before comparing
            if pixel[0] > upper_threshold and pixel[1] < lower_threshold and pixel[2] < lower_threshold:
                red_array[row_index][col_index] = 0  # updates black image if red found to show white at each red pixel

    plt.imsave("map-red-pixels.jpg", red_array, cmap='Greys')
    return red_array


def find_cyan_pixels(map_filename="./data/map.png", upper_threshold=100, lower_threshold=50):
    """
Takes an image as an input and finds all the cyan pixels in that image and marks their location in a 2D
numpy array cyan_array. cyan_array is written as an image to map-cyan-pixels.jpg where cyan pixels
are represented by white and non-cyan pixels are represented by black

     Args:
         map_filename: file location of the image used
         upper_threshold: Minimum amount of blue and green needed in a pixel to mark it as cyan
         lower_threshold: Maximum amount of red allowed in a pixel to still mark it as cyan

     Returns:
         cyan_array: 2D numpy array of 0's for cyan pixels and 1's for non-cyan pixels
     """

    rgb_img = plt.imread(map_filename)  # creates 3D numpy array of image
    height, width = rgb_img.shape[0], rgb_img.shape[1]
    cyan_array = np.array([[1] * width for _ in range(height)])  # list of 1's used as black image

    for row_index, row in enumerate(rgb_img):
        for col_index, col in enumerate(row):
            pixel = rgb_img[row_index][col_index] * 255  # multiply up rgb values before comparing
            if pixel[0] < lower_threshold and pixel[1] > upper_threshold and pixel[2] > upper_threshold:  # checks rgb values
                cyan_array[row_index][col_index] = 0  # updates black image to show white at each cyan pixel

    plt.imsave("map-cyan-pixels.jpg", cyan_array, cmap='Greys')
    return cyan_array


def detect_connected_components(map_filename="map-red-pixels.jpg", *args, **kwargs):
    """
Takes a black and white image as an input and finds the number of connected components in the image and their
sizes. Iterates through image and uses 2D array MARK to show which pixels have been visited. Each connected
component is given a unique index number which is stored in MARK in the position of each of the components pixels.
Writes every component number and its size in cc-output-2a.txt

       Args:
           map_filename: file location of the image used

       Returns:
           MARK: 2D numpy array where each pixel of each connected component is marked with the components unique index
       """

    img = plt.imread(map_filename)  # creates 3D numpy array of image
    height, width = img.shape[0], img.shape[1]

    MARK = np.array([[0] * width for _ in range(height)])  # creates 2D array of 0's with dimensions of img
    queue = []  # store pixels to visit as tuples (row index, col index)
    component_count = 0
    output_file = open("cc-output-2a.txt", "w")

    for row_index, row in enumerate(img):
        for col_index, col in enumerate(row):
            # if pixel is a pavement and is unvisited
            if img[row_index][col_index][0] > 200 and MARK[row_index][col_index] == 0:
                component_count += 1
                MARK[row_index][col_index] = component_count   # show pixel as visited by component number
                queue.append((row_index, col_index))  # add pixel coordinates to queue

                size = 1  # number of pixels in component
                while len(queue) > 0:  # once queue is 0, component is complete
                    current_pixel = queue.pop(0)  # tuple of (row_index, col_index)

                    # adds all neighbours coordinates to list 'neighbours'
                    neighbours = []  # stores coordinates of all 8 neighbours of current_pixel
                    for row_change in range(-1, 2):
                        for col_change in range(-1, 2):
                            new_row = current_pixel[0] + row_change
                            new_col = current_pixel[1] + col_change
                            # check coordinates are within image dimensions before adding to 'neighbours'
                            if 0 <= new_row < height and 0 <= new_col < width:
                                neighbours.append((new_row, new_col))
                    neighbours.remove((current_pixel[0], current_pixel[1]))  # remove coordinates of original pixel

                    # iterate through neighbours and check if they are a path and not visited
                    for neighbour in neighbours:
                        n_row, n_col = neighbour[0], neighbour[1]
                        if img[n_row][n_col][0] > 200 and MARK[n_row][n_col] == 0:
                            MARK[n_row][n_col] = component_count  # show pixel as visited by component number
                            queue.append((n_row, n_col))
                            size += 1
                output_file.write(f"Connected Component {component_count}, number of pixels = {size} \n")

    output_file.write(f"Total number of connected components = {component_count}")
    output_file.close()
    return MARK


def detect_connected_components_sorted(MARK, *args, **kwargs):
    """
Takes detect_connected_components as a parameter to get MARK which is used to generate a list of all the
connected components. Sorts components into descending order by size and writes components to cc-output-2b.txt
Creates an image of the two largest components and saves to cc-top-2.jpg

       Args:
           MARK: 2D numpy array generated by detect_connected_components

       Returns:
           top_two: 2D numpy array of two largest connected components in image
       """

    MARK_no_0 = [x for x in MARK.flatten() if x != 0]  # creates 1D array removing all 0's from MARK
    num_of_components = max(MARK_no_0)  # largest number in MARK is the number of components

    # generates list of all connected components by searching for how many times each number occurs in MARK
    component_list = []  # stores unsorted components as tuples (index, size)
    for index in range(1, num_of_components+1):
        size = utils.countvalue(MARK_no_0, index)
        component_list.append((index, size))

    # sorts components using insertion sort
    sorted_components = []
    for component in component_list:
        # if sorted_components is empty or component is larger than the largest sorted component
        if len(sorted_components) == 0 or component[1] > sorted_components[0][1]:
            sorted_components = [component] + sorted_components
        else:
            for index, _ in enumerate(sorted_components):  # compares current component with already sorted components
                if component[1] >= sorted_components[index][1]:  # if current components size >= a sorted component
                    sorted_components[index:index] = [component]  # add to sorted list just before compared component
                    break
            else:  # if loop finished without break, current component size is smaller than all components in sortedlist
                sorted_components.append(component)

    # writes components in sorted order to output file
    output_file = open("cc-output-2b.txt", "w")  # creates text file to write to
    for component in sorted_components:
        output_file.write(f"Connected Component {component[0]}, number of pixels = {component[1]}\n")
    output_file.write(f"Total number of connected components = {utils.length(sorted_components)}")
    output_file.close()

    # Generates image of largest two components
    component_1, component_2 = sorted_components[0][0], sorted_components[1][0]  # index of largest two components
    height, width = MARK.shape[0], MARK.shape[1]
    top_two = np.array([[1] * width for _ in range(height)])  # creates black image
    for row_index, row in enumerate(MARK):
        for col_index, _ in enumerate(row):
            pixel = int(MARK[row_index][col_index])
            if pixel == component_1 or pixel == component_2:  # if pixel is one of the two largest components
                top_two[row_index][col_index] = 0  # make pixel white
    plt.imsave("cc-top-2.jpg", top_two, cmap='Greys')
    return top_two
