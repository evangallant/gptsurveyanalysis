from flask import Flask, redirect, url_for, request, session, send_file, render_template
import os
from werkzeug.utils import secure_filename
import pandas as pd
import xlsxwriter

# Local libraries
import config
import aicontent
from responsemanager import response_manager
from questionanalyzer import individual_question_analyzer
from metricgenerator import metric_generator

app = Flask(__name__)
app.secret_key = "a;sldkfjb;i"
app.debug = True  # Enable debug mode for automatic reloading


# Set allowed file types
ALLOWED_EXTENSIONS = {'csv', 'xls', 'xlsx'}


# Function to check if file is of an allowed type
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=["GET", "POST"])
def index():
    # ***********  FULL ANALYSIS PATH  ***********
    if request.method == 'POST':

        # GET ALL USER INPUTS IN LOCAL MEMORY
        # Get survey data file(s) uploaded stored in local memory
        files = request.files.getlist('fileUpload[]')  # Get the list of uploaded files

        # If user submits a metrics file, read metrics for each question into a list
        metrics_file = request.files.get('metricUpload')
        if metrics_file:
            if metrics_file.filename.endswith('.csv'):
                metrics_data = pd.read_csv(metrics_file)
            elif metrics_file.filename.endswith('.xls') or metrics_file.filename.endswith('.xlsx'):
                metrics_data = pd.read_excel(metrics_file)
            metrics = metrics_data.columns.tolist()
        else:
            metrics = []

        # If user submitted the single set of example metrics, read them into memory
        example_metrics = ""
        if request.form.get('exampleMetrics'):
            example_metrics = request.form.get('exampleMetrics')

        # Get survey context from form
        survey_context = request.form.get('surveyContext')



        # Read questions into local memory (should be consistent across all survey data files)
        if files[0] and allowed_file(files[0].filename):
            if files[0].filename.endswith('.csv'):
                data = pd.read_csv(files[0])
            elif files[0].filename.endswith('.xls') or files[0].filename.endswith('.xlsx'):
                data = pd.read_excel(files[0])
            questions = data.columns.tolist()


        # If user did not upload metrics, generate them for them
        if len(metrics) == 0:
            for i in range(len(questions)):
                current_question_for_metric = questions[i]
                if not example_metrics:
                    metrics.append(metric_generator(current_question_for_metric, survey_context))
                else:
                    submitted_example_metrics = example_metrics
                    metrics.append(metric_generator(current_question_for_metric, survey_context, submitted_example_metrics))

        
        # Create excel file that will store summarized results of analysis
        # Create an empty DataFrame
        df = pd.DataFrame()

        # Create an Excel writer
        writer = pd.ExcelWriter('analysis_output.xlsx', engine='xlsxwriter')


        # Process each uploaded file
        for i, file in enumerate(files):
            if file and allowed_file(file.filename):
                # Determine file type and load data accordingly
                if file.filename.endswith('.csv'):
                    data = pd.read_csv(file)
                elif file.filename.endswith('.xls') or file.filename.endswith('.xlsx'):
                    data = pd.read_excel(file)

                # Generate the sheet name based on the index number
                sheet_name = f"Results{i + 1}"

                # Write the DataFrame to the Excel file
                df.to_excel(writer, index=False, sheet_name=sheet_name)   

                # Process the data as needed
                response_sets = []

                for column in data.columns:
                    responses = data[column][1:].tolist()  # Exclude the header row
                    response_sets.append(responses)


                # We have now separated the questions and responses into an iteratable list
                # Now we need to feed these into the question analyzer and store the final summary in a local variable
                for i in range(len(questions)):
                    current_question = questions[i]
                    current_response_set = response_sets[i]
                    current_metric = metrics[i]
                    current_question_analysis = individual_question_analyzer(survey_context, current_question, current_response_set, current_metric)


                    # After that, save the current question and output for that question to the appropriate cell in the current analysis_output file
                    current_sheet = writer.sheets[sheet_name]
                    current_sheet.write(0, i, current_question)
                    current_sheet.write(1, i, current_question_analysis)

        # Save the Excel file
        writer.close()
                
        # Return page with download buttons for output file
        return send_file('analysis_output.xlsx', as_attachment=True)

    else:
        return render_template('index.html')