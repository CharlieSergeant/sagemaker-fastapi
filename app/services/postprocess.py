def do_postprocessing(model_responses):
    sub_recommendations = []
    # ******************************************
    # Add additional post processing logic here
    # ******************************************
    for response in model_responses:
        res = round(response, 2)
        sub_recommendations.append(res)
    return sub_recommendations
