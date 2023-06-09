import tempfile
import os
import pandas as pd


from flask import Flask, request, send_file, render_template
from werkzeug.utils import secure_filename
import xlsxwriter

# Local libraries
import aicontent
import config
import openai
from prompts import iterative_thematic_prompt
from tenacity import (
    retry,
    stop_after_attempt,
    wait_random_exponential,
)  # for exponential backoff
from themesquestionanalyzer import thematic_individual_question_analyzer
from timeestimation import estimate_time

app = Flask(__name__)
app.secret_key = "a;sldkfjb;i;aoibna;b;oase;asdfa;sag;sadlhg;ashfha;;a;sdgj"
app.debug = True  # Enable debug mode for automatic reloading


# Set allowed file types
ALLOWED_EXTENSIONS = {'csv', 'xls', 'xlsx'}


# Sample survey context for sample survey data:
SAMPLE_CONTEXT_THREE_QUESTIONS_50_RESPONSES = "This survey asks people who got their taxes done for free at a VITA free tax preparation site about their experience. The goal of the survey is to understand how people benefit from getting their taxes done at a VITA site, as well as what could be improved about the process."
SAMPLE_CONTEXT_MANY_RESPONSES_ONE_QUESTION = "This single question survey asks people who got their taxes done for free at a VITA site how they plan to use their refund."

# Estimated time per prompt completion:
MINIMUM_PROMPT_COMPLETION_TIME = 10
MAXIMUM_PROMPT_COMPLETION_TIME = 50
# The average completion time is around 40 seconds, as I test this further, I should update this amount

# Token cost - Davinci 003 model
COST_PER_1000_TOKENS = .02


# Function to check if file is of an allowed type
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=["GET", "POST"])
def index():
    # ***********  FULL ANALYSIS PATH  ***********
    if request.method == 'POST':
        # GET DATA, CONTEXT, AND QUESTIONS
        # Get survey data file(s) uploaded stored in local memory in list
        files = request.files.getlist('fileUpload[]')
        if len(files) > 10:
            return "Invalid request, please submit 10 or fewer files for analysis"


        # Get survey context from form
        survey_context = request.form.get('thematicSurveyContext')


        # Get API key from user
        api_key_1 = str(request.form.get("apiKey1"))
        api_key_2 = str(request.form.get("apiKey2"))
        users_api_key = str(api_key_1 + "-" + api_key_2)
        openai.api_key = users_api_key

        action = request.form.get('action')


        if action == 'estimate':
            # Calculate time and cost estimations for all files
            total_minimum_estimated_completion_time = 0
            total_maximum_estimated_completion_time = 0
            total_estimated_cost = 0
            for i, file in enumerate(files):
                # Determine file type and load data accordingly
                if file and allowed_file(file.filename):
                    if file.filename.endswith('.csv'):
                        data = pd.read_csv(file)
                    elif file.filename.endswith('.xls') or file.filename.endswith('.xlsx'):
                        data = pd.read_excel(file)

                    # Read questions for current survey into local memory
                    questions = data.columns.tolist()
                    response_sets = []

                    for column in data.columns:
                        responses = data[column][1:].tolist()  # Exclude the header row
                        response_sets.append(responses)

                    # Calculate estimated time for completion
                    wrapper_text = iterative_thematic_prompt
                    estimated_number_prompts = estimate_time(wrapper_text, response_sets)
                    minimum_estimated_completion_time = estimated_number_prompts * MINIMUM_PROMPT_COMPLETION_TIME
                    maximum_estimated_completion_time = estimated_number_prompts * MAXIMUM_PROMPT_COMPLETION_TIME
                    total_minimum_estimated_completion_time += minimum_estimated_completion_time
                    total_maximum_estimated_completion_time += maximum_estimated_completion_time
                
                    # Calculate estimated cost for completion
                    estimated_cost = round(estimated_number_prompts * 3.8 * COST_PER_1000_TOKENS, 2)
                    total_estimated_cost += estimated_cost
            
            minimum_minutes, minimum_seconds = divmod(total_minimum_estimated_completion_time, 60)
            maximum_minutes, maximum_seconds = divmod(total_maximum_estimated_completion_time, 60)
            
            print(f"Between {minimum_minutes} minutes {minimum_seconds} seconds and {maximum_minutes} minutes {maximum_seconds} seconds estimated for completion")
            print(f"Estimated cost for completion: ${total_estimated_cost} dollars (USD)")

            return render_template('index.html', thematicSurveyContext = survey_context, apiKey1 = api_key_1, apiKey2 = api_key_2, estimated_cost = total_estimated_cost, min_minutes = minimum_minutes, min_seconds = minimum_seconds, max_minutes = maximum_minutes, max_seconds = maximum_seconds)

        elif action == 'analyze':
            # INITIALIZE OUTPUT DOC - Create excel file that will store summarized results of analysis
            # Create an empty DataFrame
            df = pd.DataFrame()

            # Create a temporary file for storing the Excel output
            with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as temp_file:
                output_filepath = temp_file.name

            # Create an Excel writer
            writer = pd.ExcelWriter(output_filepath, engine='xlsxwriter')
            wrap_format = writer.book.add_format({'text_wrap': True})



            # FOR THEMATIC ANALYSIS
            # Process each uploaded file
            for i, file in enumerate(files):
                if file and allowed_file(file.filename):
                    # Determine file type and load data accordingly
                    if file.filename.endswith('.csv'):
                        data = pd.read_csv(file)
                    elif file.filename.endswith('.xls') or file.filename.endswith('.xlsx'):
                        data = pd.read_excel(file)

                    # Read questions for current survey into local memory
                    questions = data.columns.tolist()

                    # Generate the sheet name based on the index number
                    sheet_name = f"Results{i + 1}"
                    
                    # Write the DataFrame to the Excel file
                    df.to_excel(writer, index=False, sheet_name=sheet_name)   

                    current_sheet = writer.sheets[sheet_name]
                    # Set column width and wrap text
                    for j in range(len(questions)):
                        current_sheet.set_column(j, j, 40)  # Adjust the value '20' to your desired column width


                    # Process the data as needed
                    response_sets = []

                    for column in data.columns:
                        responses = data[column][1:].tolist()  # Exclude the header row
                        response_sets.append(responses)


                    # We have now separated the questions and responses into an iteratable list
                    # Now we need to feed these into the question analyzer and store the final summary in a local variable
                    for i, question in enumerate(questions):
                        current_question = question
                        current_response_set = response_sets[i]
                        current_question_analysis = thematic_individual_question_analyzer(survey_context, current_question, current_response_set)

                        # After that, save the current question and output for that question to the appropriate cell in the current analysis_output file
                        current_sheet.write(0, i, current_question, wrap_format)
                        current_sheet.write(1, i, current_question_analysis, wrap_format)

            # Save the Excel file
            writer.close()
                    
            # Return page with download buttons for output file
            return send_file(output_filepath, as_attachment=True)
        
        else:
            return render_template('index.html')
    else:
        return render_template('index.html')