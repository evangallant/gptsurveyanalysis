import config
import aicontent
from responsemanager import response_manager

# ***********  INDIVIDUAL QUESTION ANALYZER  ***********
# Question Analyzer is a function that is called in the primary path
# Function accepts:
    # List of survey questions
    # List of survey responses
    # List of question metrics

# Load survey question, responses, and question metrics into local memory
def individual_question_analyzer(question, responses, metric):
    # Load all necessary data for current question
    current_question = question
    remaining_responses = responses
    current_question_metric = metric

    # FIRST RUN OF QUESTION ANALYZER



    # TODO: DEFINE INSTRUCTIONS FOR FIRST PROMPT
    initial_prompt_instructions = "..."



    # Batch first set of responses
    response_set, remaining_responses_new = response_manager(remaining_responses, current_question, current_question_metric, initial_prompt_instructions)

    # Call GPT API for first round of summarization (NO PREVIOUS SUMMARY)
    query = """{}
        The question is: {}
        The metrics are: {}
        This set of responses includes: {}
        """.format(initial_prompt_instructions, current_question, current_question_metric, response_set)
    previous_summary = aicontent.openAIQuery(query)



    # TODO: DEFINE ITERATIVE PROMPT INSTRUCTIONS
    iterative_prompt_instructions = "..."



    # ITERATIVE RUNS OF QUESTION ANALYZER UNTIL NO RESPONSES ARE LEFT
    while remaining_responses_new:
        # Get new set of repsonses
        response_set, remaining_responses_new = response_manager(remaining_responses_new, current_question, current_question_metric, iterative_prompt_instructions, previous_summary)

        query = """{}
        The question is: {}
        The metrics are: {}
        This set of responses includes: {}
        The previous summary for your to add to is: {}
        """.format(iterative_prompt_instructions, current_question, current_question_metric, response_set, previous_summary)
        previous_summary = aicontent.openAIQuery(query)

    return previous_summary