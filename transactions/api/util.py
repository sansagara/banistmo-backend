

def moving_av(lst, n):
    """
    Take a list lst, and return the average of its last n elements.
    """
    observations = len(lst[-n:])
    return sum(lst[-n:]) / float(observations)
