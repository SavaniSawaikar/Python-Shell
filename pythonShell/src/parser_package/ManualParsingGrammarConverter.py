'''
Converter receives an list of strings representing a command sequence, and converts it into
a Pipe or Call object depending on the overall list type (represented by its first argument). 
'''

from commands import Call, Pipe

class Converter:
    def convert_to_objects(self, command_seq):
        if not isinstance(command_seq, list):
            return command_seq
        else:
            if command_seq[0] == "Call":
                return Call(
                    command_seq[1],
                    *[self.convert_to_objects(arg) for arg in command_seq[2:]]
                )
            elif command_seq[0] == "Pipe":
                return Pipe(
                    self.convert_to_objects(command_seq[1]),
                    self.convert_to_objects(command_seq[2]),
                )
