def refine_prompt(prompt, error_type):
    
    if error_type == "Factual Error":
        return prompt + " Provide accurate and verified information with correct facts."

    elif error_type == "Hallucination":
        return prompt + " Only provide information you are certain about. Do not make up facts."

    elif error_type == "Logical Error":
        return prompt + " Explain step-by-step with clear reasoning."

    elif error_type == "Bias":
        return prompt + " Ensure the response is neutral and unbiased."

    elif error_type == "Clarity Issue":
        return prompt + " Explain clearly in simple and structured language."

    else:
        return prompt