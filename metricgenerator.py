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
    MAXIMUM_TOKENS_FOR_PROMPT = 4000
    COMPLETION_ALLOWANCE = 500
    
    # Tokenize question, context, and example metrics (if submitted)
    encoding = tiktoken.get_encoding("p50k_base")

    # Formula for getting number of tokens from .encode:
    def num_tokens_from_string(string: str, encoding_name: str) -> int:
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    number_question_tokens = num_tokens_from_string(question, "p50k_base")

    number_context_tokens = num_tokens_from_string(context, "p50k_base")

    if example_metrics:
        number_example_metrics_tokens = num_tokens_from_string(example_metrics, "p50k_base")
    else:
        number_example_metrics_tokens = 0

    # Tokenize decorative text for prompt
    filler_text = """The question is:
        The context of the survey is: 
        Some example metrics for you to base your response on are:"""
    number_filler_text_tokens = num_tokens_from_string(filler_text, "p50k_base")


    # TODO: Replace query instructions with tested prompt for metric development

    prompt = """
    You are an expert in analyzing qualitative survey data. Your role is to develop metrics for the following survey question. Make sure you structure your metrics based on the overall context of the survey. Structure your metrics so that the number of responses corresponding to each metric can be tracked. Keep in mind the process for the analysis these metrics will be used in as well - chatGPT will be conducting the analysis by accepting the survey question, the metric for that question, a small number of responses to the survey question, and a summary of the analysis from the previous set of responses. These metrics will be the basis of the analysis summary, which will be built through iterative calls to chatGPT - the previous summary will be updated with analyses from the current set of responses, then that updated summary will be iterated over with a new set of survey responses. This process continues until there are no more responses to analyze, and a full summary of all responses is created. 
    You will develop a set of metrics for this question based on the background above, as well as the survey context below, with a limit of 5 metrics. 
    You will respond only with the metrics you develop. It is important that you do not include any other filler text, or any text at all other than the metrics themselves.
    """
    number_prompt_tokens = num_tokens_from_string(prompt, "p50k_base")


    # Total tokenized allowances to determine if inputs need to be shorter
    total_allowance = (
        MAXIMUM_TOKENS_FOR_PROMPT - COMPLETION_ALLOWANCE - number_question_tokens
        - number_context_tokens - number_example_metrics_tokens - number_filler_text_tokens - number_prompt_tokens
    )

    # If token allowance exceeded, return an error
    if total_allowance <= 0:
        words_to_remove = abs(total_allowance)
        raise exceeded_allowance_error(f"Your metric development inputs exceeded the the token allowance, please remove {words_to_remove} words")


    # Assemble full prompt for metric generation
    query = """{}
        The question is: {}
        The context of the survey is: {}
        Some example metrics for you to base your response on are: {}
        """.format(prompt, question, context, example_metrics)
    metric = aicontent.openAIQuery(query)
    print(metric)


    # Return the generated metric for the question
    return metric