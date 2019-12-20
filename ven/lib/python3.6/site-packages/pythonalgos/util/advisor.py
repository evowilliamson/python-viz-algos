class Advisor(object):

    def __init__(self):
        super().__init__()

    def advise(self, advice, *args, **kwargs):
        """ Method that retrieves the advice from the subclass and executes it

        Args:
            advice(str): The string that indicates the function in the subclass
        
        """
        
        try:
            advise_function = getattr(self, advice)
            advise_function(*args, **kwargs)
        except(AttributeError):
            # TODO Why doensn't the default work
            pass

