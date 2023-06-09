import time

import aicontent
import config
import openai
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)
from prompts import initial_thematic_prompt, iterative_thematic_prompt
from responsemanager import response_manager

# ***********  INDIVIDUAL QUESTION ANALYZER  ***********
# Question Analyzer is a function that is called in the primary path
# Function accepts:
    # List of survey questions
    # List of survey responses
    # List of question metrics


# Define retry parameters
@retry(wait=wait_random_exponential(multiplier=1, max=60), stop=stop_after_attempt(10))
def openai_query_with_backoff(query):
    return aicontent.openAIQuery(query)


# Load survey question, responses, and question metrics into local memory
def thematic_individual_question_analyzer(context, question, responses):
    # Load all necessary data for current question
    current_question = question
    remaining_responses = responses
    survey_context = context

    # FIRST RUN OF QUESTION ANALYZER


    # Batch first set of responses
    response_set, remaining_responses_new = response_manager(remaining_responses, current_question, initial_thematic_prompt)

    # Call GPT API for first round of summarization (NO PREVIOUS SUMMARY)
    query = f"""{initial_thematic_prompt}
        The survey context is: {survey_context}
        The question is: {current_question}
        This set of responses includes: {response_set}
        """
    
    start_time_first_prompt = time.time()
    previous_summary = openai_query_with_backoff(query)
    end_time_first_prompt = time.time()

    execution_time = end_time_first_prompt - start_time_first_prompt


    # ITERATIVE RUNS OF QUESTION ANALYZER UNTIL NO RESPONSES ARE LEFT
    while remaining_responses_new:
        # Get new set of repsonses
        response_set, remaining_responses_new = response_manager(remaining_responses_new, current_question, iterative_thematic_prompt, previous_summary=previous_summary)

        query = f"""{iterative_thematic_prompt}
        The question is: {current_question}
        This set of responses includes: {response_set}
        The previous summary for your to add to is: {previous_summary}
        """
        start_time_iterative_prompt= time.time()
        previous_summary = openai_query_with_backoff(query)
        end_time_iterative_prompt = time.time()
        execution_time += end_time_iterative_prompt - start_time_iterative_prompt

    print(execution_time)
    final_summary = previous_summary

    return final_summary