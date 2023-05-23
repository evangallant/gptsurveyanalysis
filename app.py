from flask import Flask, render_template, redirect, url_for, request, session
import config, questionanalyzer
import aicontent
import pandas as pd
from responsemanager import response_manager
from questionanalyzer import individual_question_analyzer

app = Flask(__name__)
app.secret_key = "a;sldkfjb;i"
app.debug = True  # Enable debug mode for automatic reloading


@app.route('/analysis', methods=["GET", "POST"])
def analysis():
    # ***********  FULL ANALYSIS PATH  ***********
    if request.method = 'POST':

        # Get file(s) uploaded stored in local memory
        files = request.files.getlist('fileUpload[]')  # Get the list of uploaded files

        # Determine file types

        # If csv, load appropriately

        # If xls, load appropriately

        # If xlsx, load appropriately\
        

        # For each file, split data up into questions and responses


        # Get the questions and response sets
        questions = data.columns.tolist()
        response_sets = []

        for column in data.columns:
            responses = data[column][1:].tolist()  # Exclude the header row
            response_sets.append(responses)





        # Develop Question Metrics and store (if first run of surevey)
            # Load desired metrics categories and examples
            # For each question:
                # Run question through metric developer, feeding it:
                    # Example metrics
                    # Survey context
                    # Suggested metrics(?)
            # Store metrics in global memory + store in file t



        # Call Question Analyzer for all questions and store results

    # Return page with download buttons for output file
    return render_template('analysis.html', )