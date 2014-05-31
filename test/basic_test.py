"""
    The docstring of the **test**.
"""

def test_function(*args):
    """
    My test function.
    `args` some of those arguments.
    """
    pass

class TestClassBase:
    """
    This is the baseclass!
    """
    def __init__(self):
        """
        Initialize the class!
        """

class TestClassA(TestClassBase):
    def __init__(self):
        """
        Diferent initializer!
        """

class TestClassB(TestClassBase):
    "ClassB with function."
    def call_me(self):
        """
        Some function.
        """
