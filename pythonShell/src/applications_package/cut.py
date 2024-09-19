"""
Cut Application
===============

This class is designed to extract specified byte positions from each line of
given files or standard input and append the results to the output list.

It follows the format:
    cut -b BYTE_POS [FILE]...

    - `BYTE_POS` is the byte position(s) to extract.
    - `FILE`(s) is the name(s) of the file(s) to read from.
    - If no files are specified, uses stdin.

Static Methods:
    exec(args, out): Main method to execute the 'cut' command.
    parse_arguments(args): Parses and validates the command arguments.
    merge_intervals(intervals): Merges overlapping byte intervals.
    read_input(file_arguments, is_binary=False):
                    Reads input from files or standard input.
    extract_bytes(data, byte_positions, is_binary=False):
                    Extracts specified bytes from a line.

Raises:
    CustomFileException: For file-related exceptions.
    CustomProcessingException:
            For exceptions during byte extraction processing.
"""

import sys
import os

from custom_errors.customFileException import CustomFileException
from custom_errors.customProcessingException import CustomProcessingException


class Cut:
    @staticmethod
    def exec(args, out):
        try:
            byte_positions, file_arguments = Cut.parse_arguments(args)

            lines = Cut.read_input(file_arguments)

            for line in lines:
                extracted = Cut.extract_bytes(line, byte_positions)
                out.append(
                    extracted + "\n"
                    if extracted and extracted[-1] != "\n"
                    else extracted
                )
        except Exception as e:
            raise Exception(f"cut: {e}")

    @staticmethod
    def parse_arguments(args):
        try:
            byte_str = args[1]
            file_arguments = args[2:]

            byte_positions = []
            for part in byte_str.split(","):
                if "-" in part:
                    start, end = part.split("-")
                    start = int(start) if start else 1
                    end = int(end) if end else None
                    byte_positions.append((start, end))
                else:
                    byte_positions.append((int(part), int(part)))

            # Handle interval overlaps
            byte_positions = Cut.merge_intervals(byte_positions)

            return byte_positions, file_arguments
        except IndexError:
            raise ValueError("No byte range specified")
        except ValueError:
            raise ValueError("Invalid byte range format")

    @staticmethod
    def merge_intervals(intervals):
        # Sort intervals by their start values
        intervals.sort(key=lambda x: x[0])

        merged = []
        for interval in intervals:
            if (
                not merged
                or merged[-1][1] is None
                or interval[0] > merged[-1][1]
            ):
                merged.append(interval)
            else:
                # Merge overlapping intervals
                merged[-1] = (
                    merged[-1][0],
                    max(merged[-1][1], interval[1] or float("inf")),
                )

        # Replace 'None' or 'inf' with None again for open-ended intervals
        merged = [
            (start, None if end == float("inf") else end)
            for start, end in merged
        ]
        return merged

    @staticmethod
    def read_input(file_arguments, is_binary=False):
        lines = []
        if not file_arguments:
            # If no file arguments, read from stdin
            return (
                sys.stdin.buffer.readlines()
                if is_binary
                else sys.stdin.readlines()
            )
        for arg in file_arguments:
            if os.path.isfile(arg):
                try:
                    with open(arg, "rb" if is_binary else "r") as file:
                        lines.extend(file.readlines())
                except Exception as e:
                    raise CustomFileException(arg, e)
            else:
                # Treat non-file arguments as direct string inputs
                lines.append(arg + "\n")
        return lines

    @staticmethod
    def extract_bytes(data, byte_positions, is_binary=False):
        try:
            # Use set to avoid duplicating overlapping characters
            char_positions = set()
            for start, end in byte_positions:
                # Adjust start index for 0-based indexing
                start = max(start - 1, 0)
                end = end if end else len(data)
                char_positions.update(range(start, end))

            # Extract unique characters based on their positions
            result = "".join(
                data[i] for i in sorted(char_positions) if i < len(data)
            )
            return result
        except Exception as e:
            raise CustomProcessingException(e)
