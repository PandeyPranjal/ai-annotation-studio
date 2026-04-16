def correct_response(response, error_type):

    if error_type == "Factual Error":
        return "Correct the factual mistake and provide accurate information."

    elif error_type == "Hallucination":
        return "Remove any uncertain or made-up claims and provide only verified information."

    elif error_type == "Logical Error":
        return "Rewrite the response with clear step-by-step reasoning."

    elif error_type == "Bias":
        return "Rewrite the response in a neutral and unbiased manner."

    elif error_type == "Clarity Issue":
        return "Rewrite the response in a clear, simple, and structured way."

    else:
        return response