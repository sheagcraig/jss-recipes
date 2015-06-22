#!/usr/bin/python
# Copyright (C) 2014 Shea G Craig
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""validate_recipes.py

usage: validate_recipes.py [-h] recipe [recipe ...]

Test recipes for compliance with the jss-recipe style guide.

positional arguments:
  recipe      Path to a recipe to validate.

optional arguments:
  -h, --help  show this help message and exit
"""


import argparse
import os
import subprocess

# pylint: disable=no-name-in-module
from Foundation import (NSData,
                        NSPropertyListSerialization,
                        NSPropertyListMutableContainersAndLeaves,
                        NSPropertyListXMLFormat_v1_0)
# pylint: enable=no-name-in-module


__version__ = "0.1.0"


class Error(Exception):
    """Module base exception."""
    pass


class PlistParseError(Error):
    """Error parsing a plist file."""
    pass


class Plist(dict):
    """Abbreviated plist representation (as a dict)."""

    def __init__(self, filename=None):
        """Init a Plist, optionally from parsing an existing file.

        Args:
            filename: String path to a plist file.
        """
        if filename:
            dict.__init__(self, self.read_file(filename))
        else:
            dict.__init__(self)
            self.new_plist()

    def read_file(self, path):
        """Replace internal XML dict with data from plist at path.
        Args:
            path: String path to a plist file.

        Raises:
            PlistParseError: Error in reading plist file.
        """
        # pylint: disable=unused-variable
        info, pformat, error = (
            NSPropertyListSerialization.propertyListWithData_options_format_error_(
                NSData.dataWithContentsOfFile_(os.path.expanduser(path)),
                NSPropertyListMutableContainersAndLeaves,
                None,
                None
            ))
        # pylint: enable=unused-variable
        if info is None:
            if error is None:
                error = "Invalid plist file."
            raise PlistParseError("Can't read %s: %s" % (path, error))

        return info


class Results(object):
    """Collects test results and manages their output."""

    def __init__(self):
        self.results = []

    def add_result(self, result):
        self.results.append(result)

    def report(self, verbose=False):
        if verbose or not all((result[0] for result in self.results)):
            for result in self.results:
                if verbose or not result[0]:
                    self._print_result(result)
        else:
            print "Ok."

    def report_all(self):
        self.report(verbose=True)

    def _print_result(self, line):
        print "Test: %s Result: %s" % (line[1], line[0])


def get_argument_parser():
    """Build and return argparser for this app."""
    parser = argparse.ArgumentParser(description="Test recipes for compliance "
                                     "with the jss-recipe style guide.")
    parser.add_argument("recipe", nargs="+", help="Path to a recipe to "
                        "validate.")
    parser.add_argument("-v", "--verbose", help="Display results of all "
                        "tests.", action="store_true")
    return parser


def validate_recipe(recipe_path, verbose=False):
    """Test a recipe for compliance, printing progress.

    Args:
        recipe_path: String path to recipe file.
    """
    print_bar()
    print "Testing recipe: %s" % recipe_path

    recipe = get_recipe(recipe_path)

    results = Results()

    # Test filename and get recipe object.
    results.add_result(test_filename(recipe_path))

    tests = (test_recipe_parsing,
             test_is_in_subfolder,
             test_parent_recipe,
             test_identifier,
             test_single_processor,
             test_arguments,
             test_input_section,
             test_support_file_references,
             test_extension_attributes,
             test_scripts,
             test_icon,
             test_lint)

    for test in tests:
        result = test(recipe)
        results.add_result(result)

    if verbose:
        results.report_all()
    else:
        results.report()


def get_recipe(recipe_path):
    """Open a recipe file as an ElementTree.

    Args:
        recipe_path: String path to recipe file.

    Returns:
        ElementTree of the recipe, exception message if the recipe has parsing
        errors, or None if that file does not exist.
    """
    try:
        recipe = Plist(recipe_path)
    except IOError:
        recipe = None
    except PlistParseError as err:
        recipe = err.message

    return recipe


def test_filename(recipe_path):
    """Tests filename for correct ending.

    Args:
        recipe_path: String path to a recipe file.

    Returns:
        Tuple of Bool: Failure or success, and a string describing the
        test and result.
    """
    test = recipe_path.endswith(".jss.recipe")
    result = "Recipe has correct ending (.jss.recipe)"
    return (test, result)


def test_recipe_parsing(recipe):
    """Determine whether recipe file exists and parses.
    Args:
        recipe: Recipe object.

    Returns:
        Tuple of Bool: Failure or success, and a string describing the
        test and result.
    """
    test =False
    result = "Recipe parses correctly."
    if not recipe:
        result += " (Recipe file not found!)"
    elif isinstance(recipe, unicode):
        # There was a parsing error. Print the message and finish.
        result += " (%s)" % recipe
    else:
        test = True

    return (test, result)


def test_is_in_subfolder(recipe):
    """Determine whether recipe file exists and parses.
    Args:
        recipe: Recipe object.

    Returns:
        Tuple of Bool: Failure or success, and a string describing the
        test and result.
    """
    return (None, "Not implemented.")

# TODO: Should ensure all files in current folder have same prefix.
# TODO: And probably that none of them are PolicyTemplate,
#  SmartGroupTemplate, etc (so you don't cheat the search).

def test_parent_recipe(recipe):
    """Determine whether parent recipe is in AutoPkg org and not None.
    Args:
        recipe: Recipe object.

    Returns:
        Tuple of Bool: Failure or success, and a string describing the
        test and result.
    """
    # TODO: Make sure in AutoPkg org, and value is set!
    parent = recipe["ParentRecipe"]
    search_results = subprocess.check_output(["autopkg", "search", parent])

    test = False

    if ".pkg.recipe" in search_results:
        test =True

    return (test, "Parent Recipe is in AutoPkg org, and is set.")


def test_identifier(recipe):
    """Determine whether recipe file exists and parses.
    Args:
        recipe: Recipe object.

    Returns:
        Tuple of Bool: Failure or success, and a string describing the
        test and result.
    """
    return (None, "Not implemented.")


def test_single_processor(recipe):
    """Determine whether recipe file exists and parses.
    Args:
        recipe: Recipe object.

    Returns:
        Tuple of Bool: Failure or success, and a string describing the
        test and result.
    """
    return (None, "Not implemented.")


def test_arguments(recipe):
    """Determine whether recipe file exists and parses.
    Args:
        recipe: Recipe object.

    Returns:
        Tuple of Bool: Failure or success, and a string describing the
        test and result.
    """
    return (None, "Not implemented.")

# TODO: All values should be %ALL_CAPS%

def test_input_section(recipe):
    """Determine whether recipe file exists and parses.
    Args:
        recipe: Recipe object.

    Returns:
        Tuple of Bool: Failure or success, and a string describing the
        test and result.
    """
    return (None, "Not implemented.")

# TODO: All keys should be ALL_CAPS, and used by args, AND match the
# style guide.

def test_support_file_references(recipe):
    """Report whether all support files are referenced by filename only.

    Product Subfolder rules.

    Args:
        recipe: Recipe xml.
    """
    """Determine whether recipe file exists and parses.
    Args:
        recipe: Recipe object.

    Returns:
        Tuple of Bool: Failure or success, and a string describing the
        test and result.
    """
    # Build a list of potential xpaths to check.
    search_paths = ["Input"]
    # TODO: Not finished
    return (None, "Not implemented.")

# TODO: Make sure all input values are os.path.basename() only (uses
# search).

def test_extension_attributes(recipe):
    """Determine whether recipe file exists and parses.
    Args:
        recipe: Recipe object.

    Returns:
        Tuple of Bool: Failure or success, and a string describing the
        test and result.
    """
    return (None, "Not implemented.")

# TODO: Warn if ext attr. Test for all required files. Lint 'em.

def test_scripts(recipe):
    """Determine whether recipe file exists and parses.
    Args:
        recipe: Recipe object.

    Returns:
        Tuple of Bool: Failure or success, and a string describing the
        test and result.
    """
    return (None, "Not implemented.")

# TODO: Warn if scripts. Test for existence of referenced files. Lint
# the template.

def test_icon(recipe):
    """Determine whether recipe file exists and parses.
    Args:
        recipe: Recipe object.

    Returns:
        Tuple of Bool: Failure or success, and a string describing the
        test and result.
    """
    return (None, "Not implemented.")

# TODO: Test icon for correct size, format. Use pillow?

def test_lint(recipe):
    """Determine whether recipe file exists and parses.
    Args:
        recipe: Recipe object.

    Returns:
        Tuple of Bool: Failure or success, and a string describing the
        test and result.
    """
    return (None, "Not implemented.")

# TODO: Should probably use plutil -lint.

def print_bar():
    """Print 79 '-'s."""
    print 79 * "-"


def main():
    parser = get_argument_parser()
    args = parser.parse_args()

    # TODO: Add handling for no args (all recipes in subfolders, or
    # possibly a -r arg.
    for recipe in args.recipe:
        validate_recipe(recipe, args.verbose)


if __name__ == "__main__":
    main()