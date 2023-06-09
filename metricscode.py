
# METRICS QUESTION ANALYZER

# import config
# import aicontent
# from responsemanager import response_manager

# # ***********  INDIVIDUAL QUESTION ANALYZER  ***********
# # Question Analyzer is a function that is called in the primary path
# # Function accepts:
#     # List of survey questions
#     # List of survey responses
#     # List of question metrics

# # Load survey question, responses, and question metrics into local memory
# def metricized_individual_question_analyzer(context, question, responses, metric):
#     # Load all necessary data for current question
#     current_question = question
#     remaining_responses = responses
#     current_question_metric = metric
#     survey_context = context

#     # FIRST RUN OF QUESTION ANALYZER



#     # TODO: REFINE INSTRUCTIONS FOR FIRST PROMPT
#     initial_prompt_instructions = """
#     You are an expert at analyzing qualitative survey data. You accurately identify themes and trends in qualitative data, and are able to identify how responses correspond with key metrics. Additionally, you are an expert at keeping track of how many responses correspond to each metric. Below you will recieve the context of the survey, a survey question, metrics for that question, and a set of responses. Your primary tasks are to:
#     1) Analyze the responses and identify how they correspond to the metrics you are given.
#     2) Keep track of how many responses correspond to each level of each metric, creating a running total of the number of responses for each categorical possibility. 
#     3) Respond to this prompt with only your analysis of the responses, no other filler text. Your response should be structured around the key metrics you are given. For each metric you will respond with your running total of the number of responses for each categorical possibility. 
#     4) Find 3-5 important themes highlighted in your previous analysis. If you find more important themes in this set of responses, update this list by replacing one of the themes with the more important one. If nothing new stands out you can leave the list be.
#     5) Highlight 3 direct quotes from the responses that are noteworthy. You can decide what is noteworthy, but focus on quoting unique, interesting responses.     
#     """



#     # Batch first set of responses
#     response_set, remaining_responses_new = response_manager(remaining_responses, current_question, initial_prompt_instructions, current_question_metric)

#     # Call GPT API for first round of summarization (NO PREVIOUS SUMMARY)
#     query = f"""{initial_prompt_instructions}
#         The survey context is: {survey_context}
#         The question is: {current_question}
#         The metrics are: {current_question_metric}
#         This set of responses includes: {response_set}
#         """
#     previous_summary = aicontent.openAIQuery(query)
#     print(previous_summary)



#     # TODO: REFINE ITERATIVE PROMPT INSTRUCTIONS
#     iterative_prompt_instructions = """
#     You are an expert at analyzing qualitative survey data. You accurately identify themes and trends in qualitative data, and are able to identify how responses correspond with key metrics. Additionally, you are an expert at keeping track of how many responses correspond to each metric. Below you will recieve the context of the survey, a survey question, metrics for that question, a set of responses, and your previous analysis. Your primary tasks are to:
#     1) Analyze the responses and identify how they correspond to the metrics you are given.
#     2) Keep track of how many responses correspond to each level of each metric, creating a running total of the number of responses for each categorical possibility. 
#     3) Respond to this prompt by updating your previous analysis, include no other filler text. Your response should be structured around the key metrics you are given. For each metric you will respond with your running total of the number of responses for each categorical possibility. 
#     4) Find 3-5 important themes highlighted in your previous analysis. If you find more important themes in this set of responses, update this list by replacing one of the themes with the more important one. If nothing new stands out you can leave the list be.
#     5) Highlight 3 direct quotes from the responses that are noteworthy. You can decide what is noteworthy, but focus on quoting unique, interesting responses. 
#     """



#     # ITERATIVE RUNS OF QUESTION ANALYZER UNTIL NO RESPONSES ARE LEFT
#     while remaining_responses_new:
#         # Get new set of repsonses
#         response_set, remaining_responses_new = response_manager(remaining_responses_new, current_question, iterative_prompt_instructions, current_question_metric, previous_summary)

#         query = f"""{iterative_prompt_instructions}
#         The question is: {current_question}
#         The metrics are: {current_question_metric}
#         This set of responses includes: {response_set}
#         The previous summary for your to add to is: {previous_summary}
#         """
#         previous_summary = aicontent.openAIQuery(query)
#         print(previous_summary)

#     final_summary = previous_summary

#     return final_summary



# METRICS GENERATOR

# import aicontent
# import tiktoken

# import config

# # Metric generator is a function
#     # Accepts:
#         # current question
#         # Survey context
#         # Example metrics(?)
#     # Returns:
#         # string of metrics for that question

# class exceeded_allowance_error(Exception):
#     pass


# def metric_generator(question, context, example_metrics=None):

#     # Make sure full prompt is within token allowance
#     # Tokenize question, context, and example metrics
#     MAXIMUM_TOKENS_FOR_PROMPT = 4000
#     COMPLETION_ALLOWANCE = 500
    
#     # Tokenize question, context, and example metrics (if submitted)
#     encoding = tiktoken.get_encoding("p50k_base")

#     # Formula for getting number of tokens from .encode:
#     def num_tokens_from_string(string: str, encoding_name: str) -> int:
#         encoding = tiktoken.get_encoding(encoding_name)
#         num_tokens = len(encoding.encode(string))
#         return num_tokens

#     number_question_tokens = num_tokens_from_string(question, "p50k_base")

#     number_context_tokens = num_tokens_from_string(context, "p50k_base")

#     if example_metrics:
#         number_example_metrics_tokens = num_tokens_from_string(example_metrics, "p50k_base")
#     else:
#         number_example_metrics_tokens = 0

#     # Tokenize decorative text for prompt
#     filler_text = """The question is:
#         The context of the survey is: 
#         Some example metrics for you to base your response on are:"""
#     number_filler_text_tokens = num_tokens_from_string(filler_text, "p50k_base")


#     # TODO: Replace query instructions with tested prompt for metric development

#     prompt = """
#     You are an expert in analyzing qualitative survey data. Your role is to develop metrics for the following survey question. Make sure you structure your metrics based on the overall context of the survey. Structure your metrics so that the number of responses corresponding to each metric can be tracked. Keep in mind the process for the analysis these metrics will be used in as well - chatGPT will be conducting the analysis by accepting the survey question, the metric for that question, a small number of responses to the survey question, and a summary of the analysis from the previous set of responses. These metrics will be the basis of the analysis summary, which will be built through iterative calls to chatGPT - the previous summary will be updated with analyses from the current set of responses, then that updated summary will be iterated over with a new set of survey responses. This process continues until there are no more responses to analyze, and a full summary of all responses is created. 
#     You will develop a set of metrics for this question based on the background above, as well as the survey context below, with a limit of 5 metrics. 
#     You will respond only with the metrics you develop. It is important that you do not include any other filler text, or any text at all other than the metrics themselves.
#     """
#     number_prompt_tokens = num_tokens_from_string(prompt, "p50k_base")


#     # Total tokenized allowances to determine if inputs need to be shorter
#     total_allowance = (
#         MAXIMUM_TOKENS_FOR_PROMPT - COMPLETION_ALLOWANCE - number_question_tokens
#         - number_context_tokens - number_example_metrics_tokens - number_filler_text_tokens - number_prompt_tokens
#     )

#     # If token allowance exceeded, return an error
#     if total_allowance <= 0:
#         words_to_remove = abs(total_allowance)
#         raise exceeded_allowance_error(f"Your metric development inputs exceeded the the token allowance, please remove {words_to_remove} words")


#     # Assemble full prompt for metric generation
#     query = """{}
#         The question is: {}
#         The context of the survey is: {}
#         Some example metrics for you to base your response on are: {}
#         """.format(prompt, question, context, example_metrics)
#     metric = aicontent.openAIQuery(query)
#     print(metric)


#     # Return the generated metric for the question
#     return metric



#  APP.PY ROUTE

       # # FOR METRIC ANALYSIS
        # elif analysis_type == "metrics":
        #     # GET METRICS
        #     # If user submits a metrics file, read metrics for each question into a list
        #     metrics_file = request.files.get('metricUpload')
        #     if metrics_file:
        #         if metrics_file.filename.endswith('.csv'):
        #             metrics_data = pd.read_csv(metrics_file)
        #         elif metrics_file.filename.endswith('.xls') or metrics_file.filename.endswith('.xlsx'):
        #             metrics_data = pd.read_excel(metrics_file)
        #         metrics = metrics_data.columns.tolist()
        #     else:
        #         metrics = []

        #     # If user submitted the single set of example metrics, read them into memory
        #     example_metrics = ""
        #     if request.form.get('exampleMetrics'):
        #         example_metrics = request.form.get('exampleMetrics')

        #     # If user did not upload metrics, generate them for them
        #     if len(metrics) == 0:
        #         for i, question in enumerate(questions):
        #             current_question_for_metric = question
        #             if not example_metrics:
        #                 metrics.append(metric_generator(current_question_for_metric, survey_context))
        #             else:
        #                 metrics.append(metric_generator(current_question_for_metric, survey_context, example_metrics))


        #     # Process each uploaded file
        #     for i, file in enumerate(files):
        #         if file and allowed_file(file.filename):
        #             # Determine file type and load data accordingly
        #             if file.filename.endswith('.csv'):
        #                 data = pd.read_csv(file)
        #             elif file.filename.endswith('.xls') or file.filename.endswith('.xlsx'):
        #                 data = pd.read_excel(file)

        #             # Generate the sheet name based on the index number
        #             sheet_name = f"Results{i + 1}"

        #             # Write the DataFrame to the Excel file
        #             df.to_excel(writer, index=False, sheet_name=sheet_name)   

        #             # Process the data as needed
        #             response_sets = []

        #             for column in data.columns:
        #                 responses = data[column][1:].tolist()  # Exclude the header row
        #                 response_sets.append(responses)

        #             # Calculate estimated time for completion
        #             wrapper_text = "You are an expert at analyzing qualitative survey data. You accurately identify themes and trends in qualitative data, and are able to identify how responses correspond with key metrics. Additionally, you are an expert at keeping track of how many responses correspond to each metric. Below you will recieve the context of the survey, a survey question, metrics for that question, a set of responses, and your previous analysis. Your primary tasks are to: 1) Analyze the responses and identify how they correspond to the metrics you are given. 2) Keep track of how many responses correspond to each level of each metric, creating a running total of the number of responses for each categorical possibility. 3) Respond to this prompt by updating your previous analysis, include no other filler text. Your response should be structured around the key metrics you are given. For each metric you will respond with your running total of the number of responses for each categorical possibility. 4) Find 3-5 important themes highlighted in your previous analysis. If you find more important themes in this set of responses, update this list by replacing one of the themes with the more important one. If nothing new stands out you can leave the list be. 5) Highlight 3 direct quotes from the responses that are noteworthy. You can decide what is noteworthy, but focus on quoting unique, interesting responses."
        #             estimated_completion_time = estimate_time(wrapper_text, response_sets)


        #             # We have now separated the questions and responses into an iteratable list
        #             # Now we need to feed these into the question analyzer and store the final summary in a local variable
        #             for i, question in enumerate(questions):
        #                 current_question = question
        #                 current_response_set = response_sets[i]
        #                 current_metric = metrics[i]
        #                 current_question_analysis = metricized_individual_question_analyzer(survey_context, current_question, current_response_set, current_metric)

        #                 # After that, save the current question and output for that question to the appropriate cell in the current analysis_output file
        #                 current_sheet = writer.sheets[sheet_name]
        #                 current_sheet.write(0, i, current_question)
        #                 current_sheet.write(1, i, current_question_analysis)

        #     # Save the Excel file
        #     writer.close()
                    
        #     # Return page with download buttons for output file
        #     return send_file(output_filepath, as_attachment=True)


# HTML CODE:

    # <!-- <div id="metricsAnalysisForm">
    #   <label for="metricUpload" class="form-label"><strong>Metrics: </strong>Select the file containing your metrics (CSV or Excel), if applicable</label>
    #   <input type="file" class="form-control mb-3" id="metricUpload" name="metricUpload" accept=".csv, .xls, .xlsx">
    #   <label for="exampleMetrics" class="form-label">If you do not have a file containing metrics, copy and paste an example of a couple metrics that align with your analysis goals here. Otherwise, leave this field blank:</label>
    #   <textarea class="form-control mb-3" id="exampleMetrics" name="exampleMetrics" rows="3"></textarea>
    #   <label for="thematicSurveyContext" class="form-label">Please provide context about your survey here:</label>
    #   <textarea class="form-control mb-3" id="metricSurveyContext" name="metricSurveyContext" rows="5" required></textarea>
    # </div> -->



    #   <!-- <div class="mb-3 ml-3" id="metricsFileInstructions">
    #     <div class="row">
    #       <div class="col-lg-5">
    #         <p>
    #           <strong>Instructions for File Structure:</strong>
    #         </p>
    #         <p>
    #           This tool accepts from 1-20 files containing survey data. The files must be structured such that the survey questions are listed in the first row, and all responses for each question are listed in the column beneath the question.
    #         </p>
    #       </div>
    #       <div class="col-lg-7">
    #         Survey data file structure screenshot -->
    #         <!-- <p>
    #           <strong>Example File Structure for Survey Data:</strong>
    #         </p>
    #         <img src="static/images/Survey data format.png" alt="Example of survey data structure" class="img-fluid">
    #       </div>
    #     </div>
    #     <div class="row">
    #       <div class="col-lg-5">
    #         <p>
    #           If you are submitting a file containing metrics, please format it so that each question's metrics are listed sequentially in the first row of the file.
    #         </p>
    #       </div>
    #       <div class="col-lg-7">
    #         <p>
    #           <strong>Example File Structure for Metric Upload:</strong>
    #         </p>
    #         Metrics file structure screenshot -->
    #         <!-- <img src="static/images/metric format.png" alt="Example of metric file structure" class="img-fluid">
    #       </div>
    #     </div>
    #     <div class="row">
    #       <p><strong>Additional File Structure Considerations</strong></p><br>
    #       <p>
    #         If you are selecting multiple files, you must ensure that both the content and order of your questions are identical across all files.
    #       </p>
    #       <p>
    #         Please remember to provide rich context surrounding your survey.
    #       </p>
    #     </div>
    #   </div>  -->
  