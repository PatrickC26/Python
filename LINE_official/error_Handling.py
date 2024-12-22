
debug = True
def error_info_Handling(status_code, response_text, exception: Exception = None):
    if debug:
        print(response_text)
    if exception is not None:
        print(exception)
        print(exception.__class__)
        print("-----------\n")
    return status_code == 200