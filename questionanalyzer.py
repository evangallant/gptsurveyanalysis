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
def individual_question_analyzer(context, question, responses, metric):
    # Load all necessary data for current question
    current_question = question
    remaining_responses = responses
    current_question_metric = metric
    survey_context = context

    # FIRST RUN OF QUESTION ANALYZER



    # TODO: DEFINE INSTRUCTIONS FOR FIRST PROMPT
    initial_prompt_instructions = """
    You are an expert at analyzing qualitative survey data. You accurately identify themes and trends in qualitative data, and are able to identify how responses correspond with key metrics. Additionally, you are an expert at keeping track of how many responses correspond to each metric. Below you will recieve the context of the survey, a survey question, metrics for that question, and a set of responses. Your primary tasks are to:
    1) Analyze the responses and identify how they correspond to the metrics you are given.
    2) Keep track of how many responses correspond to each level of each metric, creating a running total of the number of responses for each categorical possibility. 
    3) Respond to this prompt with only your analysis of the responses, no other filler text. Your response should be structured around the key metrics you are given. For each metric you will respond with your running total of the number of responses for each categorical possibility. 
    4) Additionally, you will highlight 3-5 important themes distinct from the metrics that you think are valuable based on the context of the survey. 
    The survey context is: This survey looks at experiences people had getting their taxes done for free at VITA sites. Its purpose is to determine how we can improve the process and experience for our clientele. 
    The question is: How was your experience getting your taxes done? Is there anything that we can do better in the future?
    """



    # Batch first set of responses
    response_set, remaining_responses_new = response_manager(remaining_responses, current_question, current_question_metric, initial_prompt_instructions)

    # Call GPT API for first round of summarization (NO PREVIOUS SUMMARY)
    query = """{}
        The survey context is: {}
        The question is: {}
        The metrics are: {}
        This set of responses includes: {}
        """.format(survey_context, initial_prompt_instructions, current_question, current_question_metric, response_set)
    previous_summary = aicontent.openAIQuery(query)
    print(previous_summary)



    # TODO: DEFINE ITERATIVE PROMPT INSTRUCTIONS
    iterative_prompt_instructions = """
    You are an expert at analyzing qualitative survey data. You accurately identify themes and trends in qualitative data, and are able to identify how responses correspond with key metrics. Additionally, you are an expert at keeping track of how many responses correspond to each metric. Below you will recieve the context of the survey, a survey question, metrics for that question, a set of responses, and your previous analysis. Your primary tasks are to:
    1) Analyze the responses and identify how they correspond to the metrics you are given.
    2) Keep track of how many responses correspond to each level of each metric, creating a running total of the number of responses for each categorical possibility. 
    3) Respond to this prompt by updating your previous analysis, include no other filler text. Your response should be structured around the key metrics you are given. For each metric you will respond with your running total of the number of responses for each categorical possibility. 
    4) Additionally, you will find 3-5 important themes highlighted in your previous analysis. If you find more important themes in this set of responses, update this list by replacing one of the themes with the more important one. If nothing new stands out you can leave the list be.
    """



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
        print(previous_summary)

    final_summary = previous_summary

    return final_summary