def has_more_than_25_characters(string):
    """
    Check if a string has more than 25 characters.
    
    Parameters:
        string (str): The input string to check.
        
    Returns:
        bool: True if the string has more than 25 characters, False otherwise.
    """
    return len(string) > 25


def cut_string(text):
    if len(text) > 25:
        return text[:25] + "..."
    else:
        return text
