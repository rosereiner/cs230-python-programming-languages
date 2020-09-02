"""
Created on Mar 20, 2018

@author: Rose Reiner
"""
import re
import sys


def lex():
    global whole_file
    global next_token
    global next_token_type

    # four separate regexs to see if those types are matched in the file
    terminal_regex = re.compile(
        "\s*(program|begin|;|end|:=|read|\(|,|\)|write|if|then|else|while|do|\+|\-|\*|\/|=|<|>|<=|>=|\$)")  # all terminals
    constant_regex = re.compile("\s*(\d\d*)")  # any white space, a digit followed by 0 or more digits
    progname_regex = re.compile(
        "\s*([A-Z]([a-zA-Z]|\d)*)")  # any white space followed by any capital letter followed by either a [capital or lower case letter or a digit] 0 or more times
    variable_regex = re.compile(
        "\s*([a-zA-Z]([a-zA-Z]|\d)*)")  # any whitespace followed by a capital or lower case letter followed by [a capital or lower case letter or a digit] 0 or more times

    terminal = terminal_regex.match(whole_file)
    constant = constant_regex.match(whole_file)
    progname = progname_regex.match(whole_file)
    variable = variable_regex.match(whole_file)

    if terminal:  # if a terminal is found
        next_token = terminal.group(1)  # next token is assigned the part of the file that matched
        whole_file = whole_file[
                     terminal.end():]  # has lex look at the rest of the file, everything after the next_token pointer
        next_token_type = "terminal"
    elif constant:
        next_token = constant.group(1)
        whole_file = whole_file[constant.end():]
        next_token_type = "constant"
    elif progname:
        next_token = progname.group(1)
        whole_file = whole_file[progname.end():]
        next_token_type = "progname"
    elif variable:
        next_token = variable.group(1)
        whole_file = whole_file[variable.end():]
        next_token_type = "variable"
    else:
        next_token = "Invalid"


def program():
    if next_token == "program":
        lex()
        if next_token_type == "progname":
            lex()
            compound_stmt()
    else:
        error("expected \"program\", saw " + next_token)


def compound_stmt():
    if next_token == "begin":
        lex()
        stmt()
    else:
        error("expected \"begin\", saw " + next_token)

    while next_token == ";":
        lex()
        stmt()

    if next_token == "end":
        lex()
    else:
        error("expected \"end\", saw " + next_token)


def stmt():
    if next_token == "begin" or next_token == "if" or next_token == "while":
        structured_stmt()
    else:
        simple_stmt()


def simple_stmt():
    if next_token == "read":
        read_stmt()
    elif next_token == "write":
        write_stmt()
    else:
        assignment_stmt()


def write_stmt():
    if next_token == "write":
        lex()
    else:
        error("expected \"write\", saw " + next_token)
    if next_token == "(":
        lex()
        expression()
    else:
        error("expected \"(\", saw " + next_token)

    while next_token == ",":
        lex()
        expression()
        if next_token_type != "expression":
            error("expected \"expression\", saw " + next_token)

    if next_token == ")":
        lex()
    else:
        error("expected \")\", saw " + next_token)


def assignment_stmt():
    if next_token_type == "variable" or next_token_type == "progname":
        lex()
    else:
        error("expected \"variable\" or \"progname\", saw " + next_token)

    if next_token == ":=":
        lex()
        expression()
    else:
        error("expected \":=\", saw " + next_token)


def expression():
    simple_expr()
    if next_token == "=" or next_token == "<>" or next_token == "<" or next_token == ">" or next_token == "<=" or next_token == ">=":
        lex()
        simple_expr()


def simple_expr():
    if next_token == "+" or next_token == "-":
        lex()
    term()
    while next_token == "+" or next_token == "-":
        term()


def factor():
    if next_token_type == "variable" or next_token_type == "progname" or next_token_type == "constant":
        lex()
    else:
        if next_token == "(":
            lex()
            expression()
        else:
            error("expected \"(\", saw " + next_token)

        if next_token == ")":
            lex()
        else:
            error("expected \")\", saw " + next_token)


def term():
    factor()
    while next_token == "*" or next_token == "/":
        lex()
        factor()


def structured_stmt():
    if next_token == "begin":
        compound_stmt()
    if next_token == "if":
        if_stmt()
    if next_token == "while":
        while_stmt()


def if_stmt():
    if next_token == "if":
        lex()
        expression()
    else:
        error("expected \"if\", saw " + next_token)

    if next_token == "then":
        lex()
        stmt()
    else:
        error("expected \"then\", saw ", next_token)

    if next_token == "else":
        lex()
        stmt()
    else:
        error("expected \"else\", saw " + next_token)


def while_stmt():
    if next_token == "while":
        lex()
        expression()
    else:
        error("expected \"while\", saw " + next_token)

    if next_token == "do":
        lex()
        stmt()
    else:
        error("expected \"do\", saw " + next_token)


def read_stmt():
    if next_token == "read":
        lex()
    else:
        error("expected \"read\", saw " + next_token)

    if next_token == "(":
        lex()
        if next_token_type == "variable" or next_token_type == "progname":
            lex()
        else:
            error("expected \"variable\" or \"progname\", saw " + next_token)
    else:
        error("expected \"(\" saw " + next_token)

    while next_token == ",":
        lex()
        if next_token_type != "variable":
            error("expected \"variable\", saw " + next_token)

    if next_token == ")":
        lex()
    else:
        error("expected \")\", saw " + next_token)


def error(msg):
    print("Error", msg)
    sys.exit()


def main():
    global next_token
    global whole_file
    # infile = open(sys.argv[1])
    # whole_file = infile.read() + "$"
    # infile.close()

    whole_file = "program A begin read ( b ); while1do write (c)end " + "$"
    lex()
    program()

    # will show $ token at the end to know if there was a valid parse
    if next_token == "$":
        print("Valid parse")
    else:
        print("valid parse but saw extra stuff after")


main()
