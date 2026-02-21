#!/usr/bin/env python
import sys
from unittest import result
import warnings

from datetime import datetime

from coder.crew import Coder

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information


def run():
    """
    Run the crew.
    """
    inputs = {
        "assignment": "Write a Python function that takes a list of numbers and returns the sum of the squares of the numbers."
    }

    try:
        result = Coder().crew().kickoff(inputs=inputs)
        print(f"Crew result: {result}")
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


if __name__ == "__main__":
    start_time = datetime.now()
    print(f"Crew started at: {start_time}")
    run()
    end_time = datetime.now()
    print(f"Crew ended at: {end_time}")
    print(f"Total execution time: {end_time - start_time}")
