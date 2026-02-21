def sum_of_squares(numbers):
    """
    Calculate the sum of the squares of a list of numbers.

    Args:
    numbers (list of int/float): The list of numbers to be squared and summed.

    Returns:
    int/float: The sum of the squares of the numbers.
    """

    # Initialize the sum variable
    sum_squares = 0

    # Iterate through each number in the list
    for number in numbers:
        # Square the number and add it to the sum
        sum_squares += number**2

    # Return the calculated sum of squares
    return sum_squares


# Example usage
if __name__ == "__main__":
    # Define a list of numbers
    numbers = [1, 2, 3, 4, 5]

    # Print the sum of squares of the list
    print(sum_of_squares(numbers))  # Output should be 55
