class Advisor(object):

    def __init__(self):
        super().__init__()
        
    def advise(self, advice, **kwargs):
        advise_function = getattr(self, advice)
        if advise_function is None:
            return
        else:
            advise_function(**kwargs)
