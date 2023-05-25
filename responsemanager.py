import tiktoken
import openAI
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
    

def response_manager(remaining_responses, current_question, current_question_metric, prompt_instructions, previous_summary=None):
    # Define all variables and remaining response list in local memory
    MAXIMUM_TOKENS = 4000
    COMPLETION_ALLOWANCE = 500
    
    # Tokenize completion, question, metrics, instructions, and previous summary
    encoding = tiktoken.get_encoding("text-davinci-003")
    completion_tokens = encoding.encode("[Completion]")
    question_tokens = encoding.encode(current_question)
    metric_tokens = encoding.encode(current_question_metric)
    instructions_tokens = encoding.encode(prompt_instructions)
    if previous_summary:
        summary_tokens = encoding.encode(previous_summary)
    else:
        summary_tokens = []

    # Tokenize decorative text for prompt
    filler_text = """The question is: 
        The metrics are: 
        This set of responses includes:
        The previous summary for your to add to is:"""
    filler_text_tokens = encoding.encode(filler_text)
    
    # Total tokenized allowances to determine remainder available for responses
    total_allowance = (
        MAXIMUM_TOKENS - COMPLETION_ALLOWANCE - len(question_tokens)
        - len(metric_tokens) - len(instructions_tokens) - len(summary_tokens) - len(filler_text_tokens)
    )
    
    # Extract maximum amount of full responses from response list without exceeding allowance
    response_set_tokens = []
    response_set = []
    remaining_responses_new = []
    
    for response in remaining_responses:
        response_tokens = encoding.encode(response)
        
        if len(response_set_tokens) + len(response_tokens) <= total_allowance:
            response_set_tokens.extend(response_tokens)
            response_set.append(response)
        else:
            remaining_responses_new.append(response)
    
    # Return the list of maximum response set and remaining responses
    return response_set, remaining_responses_new