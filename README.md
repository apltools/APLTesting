# APLTesting

This Django application serves you tiny programming problems based on templates.
You should be able to build the docker image and run the server as usual.
Then go to https://server/entry/welcome and choose one of the tests to take them.

Currently there's no user or score management built-in, because the application seems to be best used as practice and not as formal assessment.

## Which tests are available

The database is seeded with four tests that comprise several types of questions. The questions are also provided in the database. To seed manually, use:

    python3 manage.py loaddata tests
    python3 manage.py loaddata questions

## Dependencies

As seen in the Pipfile this application depends on the unreleased interpreter for the "Basis" language.

## Acknowledgements

Application built by Björn Out with help of Jelle van Assema, Marijn Doeve and Martijn Stegeman at the University of Amsterdam.

Copyright (c) 2020--2023 University of Amsterdam.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
