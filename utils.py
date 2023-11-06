def sumvalues(values: list) -> int or float:
    """
Takes in a list and sums the elements of the list
    Args:
        values: list of integers of floats

    Returns:
        total: integer or float that is the sum of the list elements

    Raises:
        TypeError: an element in values is not an int or float
    """
    total = 0
    for value in values:
        if type(value) is int or type(value) is float:  # checks value is a number before adding
            total += value
        else:
            raise TypeError("must be only numerical values in list")
    return total


def maxvalue(values: list) -> int:
    """
Returns the index of the maximum value in a sequence. If there are multiple occurrences of the largest value, the index
of the first occurrence is returned

    Args:
        values: list of integers of floats

    Returns:
        max_index: integer index of the largest value in list

    Raises:
        TypeError: an element in values is not an int or float
        IndexError: value list is empty
    """
    if length(values) == 0:
        raise IndexError("List is empty")

    max_index = 0
    for index, value in enumerate(values):  # loops through values
        print(index)
        if type(value) is int or type(value) is float:  # checks value is a number
            if value > values[max_index]:          # if value is greater than current largest value
                max_index = index
        else:
            raise TypeError("Must be only numerical values in list")
    return max_index


def minvalue(values: list) -> int:
    """
Returns the index of the smallest value in a sequence. If there are multiple occurrences of the smallest value, the index
of the first occurrence is returned

     Args:
         values: list of integers of floats

     Returns:
         max_index: integer index of the smallest value in list

     Raises:
         TypeError: an element in values is not an int or float
         IndexError: values list is empty
     """
    if length(values) == 0:
        raise IndexError("List is empty")

    min_index = 0
    for index, value in enumerate(values):
        if type(value) is int or type(value) is float:  # checks value is a number
            if value < values[min_index]:   # if value less than current smallest value
                min_index = index
        else:
            raise TypeError("Must be only numerical values in list")
    return min_index


def meannvalue(values: list) -> float:
    """
 Returns the arithmetic mean of a list as a float. Adds up the values and divides by
the number of values in list

     Args:
         values: list of integers of floats

     Returns:
         avg: average value of all elements in the list

     Raises:
         TypeError: an element in values is not an int or float
         ZeroDivisionError: values list is empty
     """
    total = 0
    count = 0
    for value in values:
        if type(value) is int or type(value) is float:  # checks value is a number before adding
            total += value
            count += 1
        else:
            raise TypeError("must be only numerical values in list")
    try:
        avg = total / count
        return avg
    except ZeroDivisionError:
        raise ZeroDivisionError("List is empty")


def countvalue(values: list, xw) -> int:
    """
 Returns the number of times an element appears in a list

     Args:
         values: a list you want to search

     Returns:
         count: int number of times xw occurs in the list
     """
    count = 0  # stores number of times xw if found
    for value in values:
        if value == xw:
            count += 1
    return count


def length(values: list) -> int:
    """
 Returns number of elements in a sequence

     Args:
         values: sequence

     Returns:
         count: int number of elements in a list

    Raises:
        TypeError: values argument is not a sequence
     """
    count = 0
    try:
        for _ in values:
            count += 1
        return count
    except TypeError:
        raise TypeError("Non sequence passed in")


def sort_list(L):
    """
Sorts L into descending order by insertion sort. L should contain integers or floats

     Args:
         L: list of integers of floats

     Returns:
         sorted_L: L sorted into descending order
     """
    sorted_l = []
    for item in L:
        if type(item) != int and type(item) != float:
            raise TypeError("List contains non numerical value")

        if length(sorted_l) == 0:  # first element of L added to sorted_L without comparison
            sorted_l.append(item)
            continue
        for index, _ in enumerate(sorted_l):  # compares current component with already sorted components
            if item >= sorted_l[index]:
                sorted_l[index:index] = [item]  # add to sorted list just before compared component
                break
        else:  # if current component size is smaller than all components in sorted list. Loop completes without break
            sorted_l.append(item)
    return sorted_l


def median(values: list) -> float:
    """
 Returns the median of all the values in a list

     Args:
         values: list of integers of floats

     Returns:
         avg: average value of all elements in the list

     Raises:
         TypeError: an element in values is not an int or float
         IndexError: values list is empty
     """
    try:
        values = sort_list(values)
        mid = len(values) // 2
        med = (values[mid] + values[~mid]) / 2  # averages two middle elements for even length lists
        # values[mid] and values[~mid] are the same for odd length lists
        return med
    except TypeError:
        raise TypeError("input is not a list of numbers")
    except IndexError:
        raise IndexError("List is empty")


