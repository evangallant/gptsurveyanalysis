# The time estimation function calculates an estimated amount of time required to complete the analysis
# The function accepts:
    # The full set of responses (to be tokenized)
    # The the wrapper text for the prompt

import tiktoken

def estimate_time(wrapper_text, all_responses):
    # Formula for getting number of tokens from .encode:
    def num_tokens_from_string(string: str, encoding_name: str) -> int:
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens
    encoding = tiktoken.get_encoding("p50k_base")

    # For each question and that question's responses, we need to generate the number of prompts. 
    # The number of prompts should never be less than the number of questions
    # For each question, get the set of responses, then calculate the number of prompts required for that question
    # Finally we need to add the total prompts required for each question together 


    prompt_allowance = 2500 # Choosing 2500 here to allow for previous summaries and questions
    wrapper_text_allowance = num_tokens_from_string(wrapper_text, "p50k_base")
    available_tokens = prompt_allowance - wrapper_text_allowance
    number_of_prompts = 0


    # all_responses is a list of lists, where each primary list contains a list of all the responses for that question

    # For each primary list item (response set) in all_responses
    for response_set in all_responses:
        # Initialize count of tokens for current response set
        total_tokens_current_response_set = 0

        # Go through each response, get number of tokens and add to total tokens for that question's responses
        for response in response_set:
            response_string = str(response)
            current_response_tokens = num_tokens_from_string(response_string, "p50k_base")
            total_tokens_current_response_set += current_response_tokens
        
        # Once we have the total tokens for that response set, we can calculate the number of prompts needed for that question's responses
        while total_tokens_current_response_set > 0:
            # We can calculate the amount of tokens leftover for each response set by subtracting the wrapper text allowance from the total prompt allowance
            # Then we subtract that number of tokens from the total remaining tokens for the current response set and increment number_of_prompts by 1
            total_tokens_current_response_set -= available_tokens
            number_of_prompts += 1

    return number_of_prompts
