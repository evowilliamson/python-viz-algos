""" Module that defines a logging class that offers basic logging with indentation
and log yes/no switch
"""

class Logging:
    """ Class that is accessed in a static way. It contains functions for basic logging
    """

    logging = False
    inc_level = 0
    inc_size = 3

    @classmethod
    def start(cls):
        Logging.logging = True

    @classmethod
    def stop(cls):
        Logging.logging = False

    @classmethod
    def log(cls, message, *args, inc=0):
        """ Function that logs a message

        Args:
            message: The message (with placeholders) to be logged
            args: The actual values that will replace the placeholders
            inc(bool). If True, first an indent will be perfromed. If false, no indent
            
        """

        if Logging.logging:
            if (inc != -1):
                Logging.inc_level += inc
            print(" " * (Logging.inc_level * Logging.inc_size) + message.format(*args))
            if (inc == -1):
                Logging.inc_level -= 1

    @classmethod            
    def inc_indent(cls,):
        Logging.inc_level += 1

    @classmethod            
    def dec_indent(cls,):
        Logging.inc_level -= 1

    @classmethod            
    def set_inc_size(cls, size):
        Logging.inc_size = size

