def check_http_response(response, param_to_check):
    result = None

    try:
        assert param_to_check in response.text
        
    except AssertionError as err:
        response.failure(f"Assertion error: text pattern {param_to_check} was not found in text")

        
        result = False

    else:
        result = True

    return result