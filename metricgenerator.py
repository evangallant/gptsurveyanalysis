import config
import aicontent

# Add functionality for generating metrics
# Metric generator is a function
    # Accepts:
        # current question
        # Survey context
        # Example metrics(?)
    # Returns:
        # string of metrics for that question


def metric_generator(question, context, example_metrics):

    # TODO: Replace query instructions with tested prompt for metric development

    query = """You are an expert in conducting qualitative analysis on surveys. Your job is to develop rigorous, contextually
        significant metrics for the following question. Sturcture your metrics such that...


        The question is: {}
        The context of the survey is: {}
        Some example metrics for you to base your response on are: {}
        """.format(question, context, example_metrics)
    metric = aicontent.openAIQuery(query)

    return metric