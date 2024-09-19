'''
Class Evaluator receives a Call or Pipe object and calls the eval function associated with the object
to evaluate the final result.
'''

from commands import Call, Pipe

class Evaluator:
    @staticmethod
    def evaluate(convertedObject, out):
        if isinstance(convertedObject, Call) or isinstance(
            convertedObject, Pipe
        ):
            convertedObject.eval(out)
