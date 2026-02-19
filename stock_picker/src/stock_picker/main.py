#!/usr/bin/env python
import warnings


from stock_picker.crew import StockPicker

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information


def run():
    """Main function to run the StockPicker crew"""

    inputs = {
        "sector": "technology",
    }

    result = StockPicker().crew().kickoff(inputs=inputs)
    print("Crew Result:", result)


if __name__ == "__main__":
    run()
