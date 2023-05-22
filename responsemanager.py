import config
import openai

# Response manager is a function that batches questions into maximum size for token allowance
# Function accepts:
    # Remaining response list
    # Completion allowance
    # Question allowance
    # Metrics allowance
    # Instructions allowance
    # Previous summary allowance
# Function returns:
    # Maximum token responses set
    
# Load all allowances and remaining response list into local memory



# Tokenize completion, question, metrics, instructions, and previous summary



# Total tokenized allowances to determine remainder available for responses



# Extract maximum amount of full responses from response list without exceeding allowance



# Return that list of responses and list of remaining responses to be fed back in for the next iteration