"""
Copyright (c) 2015, Dave Mankoff
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

import pytest

from htmlmin.python3html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
    """Create parser based on https://docs.python.org/3/library/html.parser.html"""

    def handle_starttag(self, tag, attrs):
        result = f"Encountered a start tag: {tag}"
        assert result == "Encountered a start tag: html"

    def handle_endtag(self, tag):
        result = f"Encountered an end tag: {tag}"
        assert result == "Encountered an end tag: html"

    def handle_data(self, data):
        result = f"Encountered some data: {data}"
        assert result == "Encountered some data: Test"


class OtherHTMLParser(HTMLParser):
    """Create parser based on https://docs.python.org/3/library/html.parser.html"""

    def handle_starttag(self, tag, attrs):
        result = f"Encountered a start tag: {tag}"
        print(result)

    def handle_comment(self, data):
        result = f"Encountered some data: {data}"
        print(result)


class TestHTMLParser:
    @pytest.fixture(autouse=True)
    def capsys(self, capsys):
        self.capsys = capsys

    def setup_method(self):
        self.parser = MyHTMLParser()

    def test_simple_parser(self):
        self.parser.feed("<html>Test</html>")
        self.parser.close()

    def test_bogus_comment(self):
        with pytest.raises(AssertionError):
            bogus_parser = OtherHTMLParser()
            bogus_parser.feed("Tes<!-- This should be removed -->")
            bogus_parser.parse_bogus_comment(i=1)
            bogus_parser.close()
