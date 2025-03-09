#!/usr/bin/env python
"""
Copyright (c) 2013, Dave Mankoff
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
    * Redistributions of source code must retain the above copyright
      notice, this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright
      notice, this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.
    * Neither the name of Dave Mankoff nor the
      names of its contributors may be used to endorse or promote products
      derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL DAVE MANKOFF AND TATIANA SATURNO BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import os
import subprocess  # nosec
import tempfile


class TestCommand:
    def run_command(self, args, input_text=None):
        """Helper function to run the command-line script with given arguments."""
        cmd = ["python3", "-m", "htmlmin.command"] + args
        result = subprocess.run(cmd, input=input_text, text=True, capture_output=True)  # nosec
        return result.stdout.strip(), result.stderr.strip()

    def test_minification_from_stdin(self):
        """Test minification using standard input (stdin)."""
        input_html = "   <p>Hello, World!  <!-- This should be removed --> </p>   "
        expected_output = "<p>Hello, World! </p>"

        output, error = self.run_command(["-c"], input_text=input_html)

        assert error == "", f"Unexpected error: {error}"
        assert output == expected_output, f"Unexpected output: {output}"

    def test_minification_from_file(self):
        """Test minification when reading from an input file."""
        input_html = "   <p> Test  <!-- Remove me --> </p>   "
        expected_output = "<p> Test </p>"

        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".html", mode="w"
        ) as input_file:
            input_file.write(input_html)
            input_file_path = input_file.name

        with tempfile.NamedTemporaryFile(
            delete=False, suffix=".html", mode="r"
        ) as output_file:
            output_file_path = output_file.name

        try:
            self.run_command(["-c", input_file_path, output_file_path])

            with open(output_file_path, "r") as f:
                output = f.read().strip()

            assert output == expected_output, f"Unexpected output: {output}"

        finally:
            os.remove(input_file_path)
            os.remove(output_file_path)
