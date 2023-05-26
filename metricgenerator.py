import aicontent
import tiktoken

import config

# Metric generator is a function
    # Accepts:
        # current question
        # Survey context
        # Example metrics(?)
    # Returns:
        # string of metrics for that question

class exceeded_allowance_error(Exception):
    pass


def metric_generator(question, context, example_metrics=None):

    # Make sure full prompt is within token allowance
    # Tokenize question, context, and example metrics
    MAXIMUM_TOKENS = 4000
    COMPLETION_ALLOWANCE = 500
    
    # Tokenize question, metrics, instructions, and previous summary
    encoding = tiktoken.get_encoding("text-davinci-003")
    question_tokens = encoding.encode(question)
    context_tokens = encoding.encode(context)

    if example_metrics:
        example_metrics_tokens = encoding.encode(example_metrics)
    else:
        example_metrics_tokens = 0

    # Tokenize decorative text for prompt
    filler_text = """The question is:
        The context of the survey is: 
        Some example metrics for you to base your response on are:"""
    filler_text_tokens = encoding.encode(filler_text)


    # TODO: Replace query instructions with tested prompt for metric development

    prompt = """
    ...
    """
    prompt_tokens = encoding.encode(prompt)


    # Total tokenized allowances to determine if inputs need to be shorter
    total_allowance = (
        MAXIMUM_TOKENS - COMPLETION_ALLOWANCE - len(question_tokens)
        - len(context_tokens) - len(example_metrics_tokens) - len(filler_text_tokens) - len(prompt_tokens)
    )

    # If token allowance exceeded, return an error
    if total_allowance <= 0:
        words_to_remove = abs(total_allowance)
        raise exceeded_allowance_error(f"Your inputs exceed the the token allowance, please remove {words_to_remove} words")


    # Assemble full prompt for metric generation
    query = """{}
        The question is: {}
        The context of the survey is: {}
        Some example metrics for you to base your response on are: {}
        """.format(prompt, question, context, example_metrics)
    metric = aicontent.openAIQuery(query)


    # Return the generated metric for the question
    return metric