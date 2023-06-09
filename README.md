# gptsurveyanalysis
OVERVIEW
This survey analysis tool uses iterative OpenAI API calls to analyze qualitative survey data, extract themes, and highlight relevant quotes. It is built within a simple flask app 
which you can run on a local host - since the API is called on the backend, as long as you have internet connection the tool will function.


USAGE
This tool accepts qualitative survey data in the form of csv or excel files (up to 10 files). The structure of the file is integral to proper functioning of the tool.
1) Upload your survey data (conforming to the data structure conventions below) and input your survey context
2) If you would like, click the 'Estimate Cost and Completion Time' button, to see estimated values for the cost and amount of time needed for completion.
3) Enter your OpenAI API key (you must enable billing in order for the API key to function) - see COST for more information
4) Click analyze. 

Some API requests are completed in a short amount of time (15 seconds), others may take longer (up to 100 seconds).

Once completed, your final analysis file will be sent to the flask page, where you can download it. 


COST
This tool uses OpenAI's API, which costs money. Utilize the 'Estimate Cost and Completion Time' button to get a sense of how much the analysis will cost. 
OpenAI's costs are based on the amount of tokens in a prompt. Tokens represent strings of characters, so the cost increases as you analyze more data.
API pricing: https://openai.com/pricing

Since we use the Davinci model to maximize accuracy and analysis complexity, the cost is: $0.0200 / 1,000 tokens
For example, in a short survey with 3 questions, each with 50 short answer responses, the cost of analysis is around $0.20. 


DATA STRUCTURE CONVENTIONS
Your survey data files must conform strictly to the following conventions. If they do not, the tool will be unable to accurately determine what are questions and what are responses.
1) Your files must contain only one tab of data
2) Your files must contain only survey questions and responses to those questions
3) Your survey questions must be in the first row (header) of the file (i.e., in an excel spreadsheet, your questions will be in cells A1, B1, C1, etc.)
4) The responses to your survey questions must be in the columns beneath the corresponding question (i.e., in an excel spreadsheet, the responses to question 1 will be in cells A2, A3, A4, etc, the responses to question 2 will be in cells B2, B3, B4, etc., and so on)


FUNCTIONALITY
The tool is built on two main functions:
1) A Response Manager, which extracts a set of responses from the survey data. To do so, the function tokenizes the current prompt and the survey responses in order to create sets of responses that fit within the 4097 token limit for each prompt. 
2) A Question Analyzer, which concatenates the analysis prompt, survey context, current survey question, and current set of survey responses from the Response Manager into a cohesive prompt. Since multiple prompts are required to analyze any substantial amount of survey data, this function has two parts:
    a) Initial prompting, which instructs the model to generate a summary of the analysis of the first set of responses, and
    b) Iterative prompting, which also accepts previous analysis summaries. The model builds off of previous summaries, then outputs an updated summary. This process continues until
        the Response Manager has no more survey data to batch out.

By using these functions in tandem we can iterate over all the survey data in all the files, one question at a time, and generate summaries that are fed into an outputted spreadsheet.
        
Additional accessory functions include:
1) Time Estimation, which tokenizes the input and calculates an estimated amount of time until completion based on average past completion times
2) Exponential Backoff from the Tenacity library, which, in the event of a RateLimitError or other error from OpenAI, retries the analysis until it is successful.
3) Metric paths and accessory functions, which are stored in the metricscode.py. These are deprecated, but you can integrate them into the app.py file if you want to try experimental metric development processes facilitated by OpenAI's API as well. They need refactoring and logic integration to be functional if included.


LIMITATIONS
***IMPORTANT*** Since the model is a generative AI, it is not built to count items. Thus, even when explicitly prompted, it is unable to generate quantitative statistics on the number of responses that correlate to each theme. This tool is to be exclusively for identifying themes and extracting relevant quotes. But honestly, if you can figure out how to make it do this let me know. So far I have tried the following appraoches, both individually and in combination:
    Explicitly numbering each response
    Adding unique characters to identify where one response ends and another begins
    Instructing the model to increment a specific variable when it identifies a response that correlates to a given theme


This tool is well suited to identifying themes from survey data with relatively short responses. Due to the prompt length limits of the model, full interviews, or long open response questions are better suited for manual analysis. 

Since the tool relies on the OpenAI API to function, and since the API incurs a cost to call, it is unadvised to submit extremely large amounts of data for analysis. If you do so by accident, simply use ctr+c to stop the program in the terminal.


TOKENIZATION
This tool utilizes OpenAI's Tiktoken library, which is contains a function that calculates the number of tokens for a given string of text. By using this tool, we can:
    Make use of the Response Manager to extract responses sets
    Calculate an estimated cost for the analysis
    Calculate the estimated amount of time required to complete the analysis


MODEL INFORMATION
This tool utilizes OpenAI's text-davinci-003 model, which is well suited to generating comprehensive summaries of long, complex text inputs.

The text-davinci-003 model is restricted to a maximum of 4097 tokens per prompt.

Model parameters are set to:
      temperature=0.5,
      max_tokens=1000,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0

These parameters can be edited in the aicontent.py module.
