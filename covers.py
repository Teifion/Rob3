"""
covers.py - Alpha version

This code is released as-is with no warranty of any sort. You are welcome to alter and distribute though I'd always appriciate credit being given if possible.

Written by Teifion Jordan (http://woarl.com)
"""

import os
import re
import unittest
from collections import OrderedDict

get_module_name = re.compile(r'.*?/?(.*?)\.py')

def get_coverage(test_program, root_dir, verbose = True, module_skip = [], dirs_skip = []):
    modules = OrderedDict()
    module_skip.extend(["__init__", "covers"])
    
    # First we need a list of all the modules we want to look at, we simply walk through all folders in the root directory
    for root, dirs, files in os.walk(root_dir):
        for d in dirs_skip:
            if d in dirs: dirs.remove(d)
        
        folder = root.replace(root_dir, "")
        for f in files:
            # We only want to look at python files
            if "".join(f[-3:len(f)]) == '.py':
                file_name = get_module_name.search(f)
                if file_name != None:
                    file_name = file_name.groups()[0].strip()
                else:
                    raise Warning("The file {0} passed the .py test but no match was found".format(f))
                
                if file_name in module_skip:
                    continue
                
                # Now to actually import it
                if folder == "":
                    try:
                        coverage_module = __import__(file_name)
                    except ImportError as e:
                        print("Error importing {0}".format(file_name))
                        raise
                else:
                    try:
                        coverage_module = __import__(folder.replace("/", ""), fromlist=[file_name])
                        coverage_module = getattr(coverage_module, file_name)
                    except ImportError as e:
                        print("Error importing {0}.{1}".format(folder.replace("/", ""), file_name))
                        raise
                
                # Now we add it to our list
                modules[(folder, file_name)] = coverage_module
    
    # Examine the test result data
    test_program_info = get_test_targets(test_program.test)
    
    # Stats
    covered = 0
    total = 0
    red, yellow, green = 0, 0, 0
    
    # Run through each module to get all classes and functions
    last_folder = ''
    print("/")
    for path, the_module in modules.items():
        folder, module_name = path
        
        # We need to print the folder we're looking into
        if last_folder != folder:
            last_folder = folder
            print("\n{0}".format(folder))
        
        # Look at this module and work out what we've covered in it
        line, temp_covered, temp_total = evaluate_module(module_name, the_module, test_program_info, verbose)
        if line:
            print(line)
        
        # Stats stuff
        covered += temp_covered
        total += temp_total
        
        if temp_total == 0: continue
        if temp_covered < temp_total:
            if temp_covered > 0:
                yellow += 1
            else:
                red += 1
        else:
            green += 1
    
    # Now print out final verdict
    print("")
    print("%d out of %d (%d%%)" % (covered, total, ((covered/total)*100)))
    print("%d greens" % green)
    print("%d yellows" % yellow)
    print("%d reds" % red)

def get_tests(test_suite):
    """Get all the tests we ran, then we can work out what we didn't run"""
    tests = []
    
    # it should be a unittest.TestCase
    if type(test_suite) != unittest.TestSuite:
        return [test_suite]
    
    for t in test_suite:
        tests.extend(get_tests(t))
    
    return tests

def get_test_targets(test_suite):
    tests = get_tests(test_suite)
    targets = set()
    
    for t in tests:
        try:
            for f in t.test_targets:
                targets.add(f)
        except AttributeError as e:
            # It's assumed that it has no targets
            pass
    
    return list(targets)

def get_functions(the_module):
    functions = []
    for d in dir(the_module):
        f = getattr(the_module, d)
        
        # If it's a function we add it to the list
        if str(f.__class__) == "<class 'function'>":
            if f.__module__ == the_module.__name__:
                functions.append(f)
        elif str(f.__class__) == "<class 'type'>":
            # If it's a class and from this module then want both it and any functions it may have
            if f.__module__ == the_module.__name__:
                functions.append(f)
                functions.extend(get_type_functions(the_module, f))
    
    return functions

def get_type_functions(the_module, the_type):
    functions = []
    
    for d in dir(the_type):
        f = getattr(the_type, d)
        
        if str(f.__class__) == "<class 'function'>":
            if f.__name__ != '__init__':
                if f.__module__ == the_module.__name__:
                    functions.append(f)
    
    return functions

def evaluate_module(module_name, the_module, test_program_info, verbose=False):
    output = []
    functions = get_functions(the_module)
    
    # Empty function allows us to call it off early
    if functions == []:
        if verbose:
            return "  %s has no functions" % module_name, 0, 0
        else:
            return None, 0, 0
    
    # Each function/class that's part of the module
    covered_functions = 0
    for f in functions:
        if f in test_program_info:
            covered_functions += 1
            output.append(colour_text("    [g]%s[/g]" % f.__name__))
        else:
            output.append(colour_text("    [r]%s[/r]" % f.__name__))
    
    # At the top of the pile is the module name and it's stats
    if covered_functions < len(functions):
        if covered_functions > 0:
            h = colour_text("  [y]%s[/y] (%d/%d)" % (module_name, covered_functions, len(functions)))
        else:
            h = colour_text("  [r]%s[/r] (%d/%d)" % (module_name, covered_functions, len(functions)))
    else:
        h = colour_text("  [g]%s[/g] (%d/%d)" % (module_name, covered_functions, len(functions)))
    
    # And now we bundle it all up
    if verbose:
        output.insert(0, h)
        return "\n".join(output), covered_functions, len(functions)
    else:
        return h, covered_functions, len(functions)
    
    

shell_patterns = (
    (re.compile(r"''([^']*)''"),        '\033[1;1m\\1\033[30;0m'),
    (re.compile(r'__([^_]*)__'),        '\033[1;4m\\1\033[30;0m'),
    (re.compile(r"\*\*([^*]*)\*\*"),    '\033[1;5m\\1\033[30;0m'),
    
    (re.compile(r"\[r\](.*?)\[\/r\]"),  '\033[31m\\1\033[30;0m'),
    (re.compile(r"\[g\](.*?)\[\/g\]"),  '\033[32m\\1\033[30;0m'),
    (re.compile(r"\[y\](.*?)\[\/y\]"),  '\033[33m\\1\033[30;0m'),
    (re.compile(r"\[b\](.*?)\[\/b\]"),  '\033[34m\\1\033[30;0m'),
    (re.compile(r"\[m\](.*?)\[\/m\]"),  '\033[35m\\1\033[30;0m'),
    (re.compile(r"\[c\](.*?)\[\/c\]"),  '\033[36m\\1\033[30;0m'),
)

def colour_text(text):
    """
    Converts text to display in the shell with pretty colours
    
    Bold:           ''{TEXT}''
    Underline:      __{TEXT}__
    Blink:          **{TEXT}**
    
    Colour:         [colour]{TEXT}[/colour]
    Colours supported: Red, Green, Yellow, Blue, Magenta, Cyan
    """
    if type(text) != str:
        return text
    
    for regex, replacement in shell_patterns:
        text = regex.sub(replacement, text)
    
    return text
