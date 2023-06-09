import tiktoken
import config

# Response manager is a function that returns the maximum amount of responses from a full response set based on the 
# tokenized allowances of the components of the prompt, and the maximum tokens available per prompt.
# Function accepts:
    # Remaining response list (EACH RESPONSE IS A LIST ITEM)
    # Completion allowance
    # Question allowance
    # Metrics allowance
    # Instructions allowance
    # Previous summary allowance
# Function returns:
    # Maximum token responses set
    # Remaining response list
    

def response_manager(remaining_responses, current_question, prompt_instructions, previous_summary=None):
    # Define all variables and remaining response list in local memory
    MAXIMUM_TOKENS = 3097
    COMPLETION_ALLOWANCE = 1000

    # Formula for getting number of tokens from .encode:
    def num_tokens_from_string(string: str, encoding_name: str) -> int:
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens
    
    # Tokenize question, metrics, instructions, and previous summary
    encoding = tiktoken.get_encoding("p50k_base")
    number_question_tokens = num_tokens_from_string(current_question, "p50k_base")

    number_instructions_tokens = num_tokens_from_string(prompt_instructions, "p50k_base")

    if previous_summary:
        number_summary_tokens = num_tokens_from_string(previous_summary, "p50k_base")
    else:
        number_summary_tokens = 0


    # Tokenize decorative text for prompt
    filler_text = """The question is: 
        This set of responses includes:
        The previous summary for your to add to is:"""
    number_filler_text_tokens = num_tokens_from_string(filler_text, "p50k_base")
    
    # Total tokenized allowances to determine remainder available for responses
    total_allowance = (
        MAXIMUM_TOKENS - COMPLETION_ALLOWANCE - number_question_tokens
        - number_instructions_tokens - number_summary_tokens - number_filler_text_tokens
    )
    
    # Extract maximum amount of full responses from response list without exceeding allowance
    # Extract maximum amount of full responses from response list without exceeding allowance
    response_set_tokens = 0
    response_set = []
    response_indices_included = []

    for i, response in enumerate(remaining_responses):
        response_str = str(response)
        response_tokens = num_tokens_from_string(response_str, "p50k_base")

        if response_set_tokens + response_tokens < total_allowance:
            response_set_tokens += response_tokens
            response_set.append(response_str + ' ~')  # Append the '~' to each response so the model knows where one response begins and ends.
            response_indices_included.append(i)

    # Remove the responses from 'remaining_responses_new' that were included in 'response_set'
    remaining_responses_new = [response for i, response in enumerate(remaining_responses) if i not in response_indices_included]

    # Return the list of maximum response set and remaining responses
    return response_set, remaining_responses_new