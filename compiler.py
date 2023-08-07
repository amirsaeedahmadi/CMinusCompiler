from scanner.scanner import Scanner
from scanner.DFA import DFA, TokenType, Transition, State
from parser.TD import TD, Node, Pattern, TerminalTransition, NonTerminalTransition, EpsilonPattern, EpsilonTransition
import re
from typing import Dict
from enum import Enum


# read input
input_file = open("input.txt", "r")
input_lines_string = input_file.read()
tokens_list = [[]]
symbol_table_list = ["break", "else", "if", "int", "repeat", "return", "until", "void", ]
lexical_errors_list = {}
INVALID_INPUT = r'[^a-zA-Z0-9;:,\[\]\(\)\{\}\+\-<=\*/\s]'

# grammer production names:

class ProductionNames(Enum):
    program = 'program'
    declaration_list = 'declaration_list'
    declaration = 'declaration'
    declaration_initial = 'declaration_initial'
    declaration_prime = 'declaration_prime'
    var_declaration_prime = 'var_declaration_prime'
    fun_declaration_prime = 'fun_declaration_prime'
    type_specifier = 'type_specifier'
    params = 'params'
    param_list = 'param_list'
    param = 'param'
    param_prime = 'param_prime'
    compound_stmt = 'compound_stmt'
    statement_list = 'statement_list'
    statement = 'statement'
    expression_stmt = 'expression_stmt'
    selection_stmt = 'selection_stmt'
    else_stmt = 'else_stmt'
    iteration_stmt = 'iteration_stmt'
    return_stmt = 'return_stmt'
    return_stmt_prime = 'return_stmt_prime'
    expression = 'expression'
    B = 'B'
    H = 'H'
    simple_expression_zegond = 'simple_expression_zegond'
    simple_expression_prime = 'simple_expression_prime'
    C = 'C'
    relop = 'relop'
    additive_expression = 'additive_expression'
    additive_expression_prime = 'additive_expression_prime'
    additive_expression_zegond = 'additive_expression_zegond'
    D = 'D'
    addop = 'addop'
    term = 'term'
    term_prime = 'term_prime'
    term_zegond = 'term_zegond'
    G = 'G'
    factor = 'factor'
    var_call_prime = 'var_call_prime'
    var_prime = 'var_prime'
    factor_prime = 'factor_prime'
    factor_zegond = 'factor_zegond'
    args = 'args'
    arg_list = 'arg_list'
    arg_list_prime = 'arg_list_prime'
    

# creating TDs

def create_td():
    info_dict = dict(
        program = TD(
            first_node = Node(1, False, False,), 
            final_node_number = 3,  # EOF at the end
            scanner = scanner, 
            first = [
                
                Pattern(type = TokenType.EOF),
                Pattern(type = TokenType.KEYWORD, regex = r'(int|void)')
            ],
            follow = None, 
            terminal_transitions = [
                TerminalTransition(2, 3, None, type = TokenType.EOF)
            
            ],
            non_terminal_transitions = [
                NonTerminalTransition(1, 2, value = ProductionNames.declaration_list.value)
            ],
            epsilon_transitions = None
        ),           
        declaration_list = TD(
            first_node = Node(1, False, False,), 
            final_node_number = 3, 
            first=[
                Pattern(type = TokenType.KEYWORD, regex = r'(int|void)'),
                EpsilonPattern(),
            ],
            follow=[
                Pattern(type = TokenType.EOF),
                Pattern(type = TokenType.SYMBOL, regex = r'(;|\(|{|})'),
                Pattern(type = TokenType.KEYWORD, regex = r'(break|if|repeat|return)'),
                Pattern(type = TokenType.ID),
                Pattern(type = TokenType.NUM),
            ],
            non_terminal_transitions=[
                NonTerminalTransition(1, 2, None, value = ProductionNames.declaration.value),
                NonTerminalTransition(2, 3, None, value = ProductionNames.declaration_list.value),
            ],
            epsilon_transitions=[
                EpsilonTransition(1, 3, None),
            ]
        ),
        declaration = TD(
            first_node = Node(1, False, False,), 
            final_node_number = 3, 
            first=[
                Pattern(type = TokenType.KEYWORD, regex = r'(int|void)'),
            ],
            follow=[
                Pattern(type = TokenType.EOF),
                Pattern(type = TokenType.SYMBOL, regex = r'(;|\(|{|})'),
                Pattern(type = TokenType.KEYWORD, regex = r'(break|if|repeat|return|int|void)'),
                Pattern(type = TokenType.ID),
                Pattern(type = TokenType.NUM),
            ],
            non_terminal_transitions=[
                NonTerminalTransition(1, 2, value = ProductionNames.declaration_initial.value),
                NonTerminalTransition(2, 3, value = ProductionNames.declaration_prime.value),
            ],
        ),
        declaration_initial = TD(
            first_node = Node(1, False, False,), 
            final_node_number = 3, 
            first=[
                Pattern(type = TokenType.KEYWORD, regex = r'(int|void)'),
            ],
            follow=[
                Pattern(type = TokenType.SYMBOL, regex = r'(\(|\)|\[|;|,)'),
            ],
            non_terminal_transitions=[
                NonTerminalTransition(1, 2, value = 'type_specifieregex = r'),
            ],
            terminal_transitions=[
                TerminalTransition(2, 3, type = TokenType.ID),
            ]
        ),
        declaration_prime = TD(
            first_node = Node(1, False, False,), 
            final_node_number = 2,
            first=[
                Pattern(type = TokenType.SYMBOL, regex = r'(\(|\[|;)'),
            ],
            follow=[
                Pattern(type = TokenType.EOF),
                Pattern(type = TokenType.SYMBOL, regex = r'(;|\(|{|})'),
                Pattern(type = TokenType.KEYWORD, regex = r'(break|if|repeat|return|int|void)'),
                Pattern(type = TokenType.ID),
                Pattern(type = TokenType.NUM),
            ],
            non_terminal_transitions=[
                NonTerminalTransition(1, 2, value = ProductionNames.fun_declaration_prime.value),
                NonTerminalTransition(1, 2, value = ProductionNames.var_declaration_prime.value),
            ],
        ),
        var_declaration_prime = TD(
            first_node = Node(1, False, False,), 
            final_node_number = 5,
            first=[
                Pattern(type = TokenType.SYMBOL, regex = r'(;|\[)'),
            ],
            follow=[
                Pattern(type = TokenType.EOF),
                Pattern(type = TokenType.SYMBOL, regex = r'(;|\(|{|})'),
                Pattern(type = TokenType.KEYWORD, regex = r'(break|if|repeat|return|int|void)'),
                Pattern(type = TokenType.ID),
                Pattern(type = TokenType.NUM),
            ],
            terminal_transitions=[
                TerminalTransition(1, 2, type = TokenType.SYMBOL, value = '['),
                TerminalTransition(2, 3, type = TokenType.NUM),
                TerminalTransition(3, 4, type = TokenType.SYMBOL, value = ']'),
                TerminalTransition(4, 5, type = TokenType.SYMBOL, value = ';'),
                TerminalTransition(1, 5, type = TokenType.SYMBOL, value = ';'),
            ],
        ),
        fun_declaration_prime = TD(
            first_node = Node(1, False, False,), 
            final_node_number = 5,
            first=[
                Pattern(type = TokenType.SYMBOL, regex = r'\('),
            ],
            follow=[
                Pattern(type = TokenType.EOF),
                Pattern(type = TokenType.SYMBOL, regex = r'(;|\(|{|})'),
                Pattern(type = TokenType.KEYWORD, regex = r'(break|if|repeat|return|int|void)'),
                Pattern(type = TokenType.ID),
                Pattern(type = TokenType.NUM),
            ],
            non_terminal_transitions=[
                NonTerminalTransition(2, 3, value = ProductionNames.params.value),
                NonTerminalTransition(4, 5, value = ProductionNames.compound_stmt.value),
            ],
            terminal_transitions=[
                TerminalTransition(1, 2, type = TokenType.SYMBOL, value = '('),
                TerminalTransition(3, 4, type = TokenType.SYMBOL, value = ')'),
            ],
        ),
        type_specifier = TD(
            first_node = Node(1, False, False,), 
            final_node_number = 2,
            first=[
                Pattern(type = TokenType.KEYWORD, regex = r'(int|void)'),
            ],
            follow=[
                Pattern(type = TokenType.ID),
            ],
            terminal_transitions=[
                TerminalTransition(1, 2, type = TokenType.KEYWORD, value = 'int'),
                TerminalTransition(1, 2, type = TokenType.KEYWORD, value = 'void'),
            ],
        ),
        params = TD(
            first_node = Node(1, False, False,), 
            final_node_number =  5,
            first=[
                Pattern(type = TokenType.KEYWORD, regex = r'(int|void)'),
            ],
            follow=[
                Pattern(type = TokenType.SYMBOL, regex = r'\)'),
            ],
            non_terminal_transitions=[
                NonTerminalTransition(3, 4, value = ProductionNames.param_prime.value),
                NonTerminalTransition(4, 5, value = ProductionNames.param_list.value),
            ],
            terminal_transitions=[
                TerminalTransition(1, 2, type = TokenType.KEYWORD, value = 'int'),
                TerminalTransition(2, 3, type = TokenType.ID),
                TerminalTransition(1, 5, type = TokenType.KEYWORD, value = 'void'),
            ],
        ),
        param_list = TD(
            first_node = Node(1, False, False,), 
            final_node_number = 4,
            first=[
                EpsilonPattern(),
                Pattern(type = TokenType.SYMBOL, regex = r','),
            ],
            follow=[
                Pattern(type = TokenType.SYMBOL, regex = r'\)'),
            ],
            non_terminal_transitions=[
                NonTerminalTransition(2, 3, value = ProductionNames.param.value),
                NonTerminalTransition(3, 4, value = ProductionNames.param_list.value),
            ],
            terminal_transitions=[
                TerminalTransition(1, 2, type = TokenType.SYMBOL, value = ','),
            ],
            epsilon_transitions=[
                EpsilonTransition(1, 4),
            ],
        ),
        param = TD(
            first_node = Node(1, False, False,), 
            final_node_number = 3, 
            first=[
                Pattern(type = TokenType.KEYWORD, regex = r'(int|void)'),
            ],
            follow=[
                Pattern(type = TokenType.SYMBOL, regex = r'(,|\))'),
            ],
            non_terminal_transitions=[
                NonTerminalTransition(1, 2, value = ProductionNames.declaration_initial.value),
                NonTerminalTransition(2, 3, value = ProductionNames.param_prime.value),
            ],
        ),
        param_prime = TD(
            first_node = Node(1, False, False,), 
            final_node_number = 3, 
            first=[
                EpsilonPattern(),
                Pattern(type = TokenType.SYMBOL, regex = r'\['),
            ],
            follow=[
                Pattern(type = TokenType.SYMBOL, regex = r'(,|\))'),
            ],
            terminal_transitions=[
                TerminalTransition(1, 2, type = TokenType.SYMBOL, value = '['),
                TerminalTransition(2, 3, type = TokenType.SYMBOL, value = ']'),
            ],
            epsilon_transitions=[
                EpsilonTransition(1, 3),
            ],
        ),
        compound_stmt = TD(
            first_node = Node(1, False, False,), 
            final_node_number = 5,
            first=[
                Pattern(type = TokenType.SYMBOL, regex = r'{'),
            ],
            follow=[
                Pattern(type = TokenType.EOF),
                Pattern(type = TokenType.SYMBOL, regex = r'(;|\(|{|})'),
                Pattern(type = TokenType.KEYWORD, regex = r'(break|if|repeat|return|int|void|endif|else|until)'),
                Pattern(type = TokenType.ID),
                Pattern(type = TokenType.NUM),
            ],
            non_terminal_transitions=[
                NonTerminalTransition(2, 3, value = ProductionNames.declaration_list.value),
                NonTerminalTransition(3, 4, value = ProductionNames.statement_list.value),
            ],
            terminal_transitions=[
                TerminalTransition(1, 2, type = TokenType.SYMBOL, value = '{'),
                TerminalTransition(4, 5, type = TokenType.SYMBOL, value = '}'),
            ],
        ),
        statement_list = TD(
            first_node = Node(1, False, False,), 
            final_node_number = 3, 
            first=[
                EpsilonPattern(),
                Pattern(type = TokenType.SYMBOL, regex = r'({|\(|;)'),
                Pattern(type = TokenType.KEYWORD, regex = r'(break|if|repeat|return)'),
                Pattern(type = TokenType.ID),
                Pattern(type = TokenType.NUM),
            ],
            follow=[
                Pattern(type = TokenType.SYMBOL, regex = r'}'),
            ],
            non_terminal_transitions=[
                NonTerminalTransition(1, 2, value = ProductionNames.statement.value),
                NonTerminalTransition(2, 3, value = ProductionNames.statement_list.value),
            ],
            epsilon_transitions=[
                EpsilonTransition(1, 3),
            ],
        ),
        statement = TD(
            first_node =2,
            final_node_number = 2,
            first=[
                Pattern(type = TokenType.SYMBOL, regex = r'({|\(|;)'),
                Pattern(type = TokenType.KEYWORD, regex = r'(break|if|repeat|return)'),
                Pattern(type = TokenType.ID),
                Pattern(type = TokenType.NUM),
            ],
            follow=[
                Pattern(type = TokenType.SYMBOL, regex = r'({|}|\(|;)'),
                Pattern(type = TokenType.KEYWORD, regex = r'(break|if|repeat|return|endif|else|until)'),
                Pattern(type = TokenType.ID),
                Pattern(type = TokenType.NUM),
            ],
            non_terminal_transitions=[
                NonTerminalTransition(1, 2, value = ProductionNames.expression_stmt.value),
                NonTerminalTransition(1, 2, value = ProductionNames.compound_stmt.value),
                NonTerminalTransition(1, 2, value = ProductionNames.selection_stmt.value),
                NonTerminalTransition(1, 2, value = ProductionNames.iteration_stmt.value),
                NonTerminalTransition(1, 2, value = ProductionNames.return_stmt.value),
            ],
        ),
        expression_stmt = TD(
            first_node = Node(1, False, False,), 
            final_node_number = 3, 
            first=[
                Pattern(type = TokenType.SYMBOL, regex = r'(\(|;)'),
                Pattern(type = TokenType.KEYWORD, regex = r'break'),
                Pattern(type = TokenType.ID),
                Pattern(type = TokenType.NUM),
            ],
            follow=[
                Pattern(type = TokenType.SYMBOL, regex = r'({|}|\(|;)'),
                Pattern(type = TokenType.KEYWORD, regex = r'(break|if|repeat|return|endif|else|until)'),
                Pattern(type = TokenType.ID),
                Pattern(type = TokenType.NUM),
            ],
            non_terminal_transitions=[
                NonTerminalTransition(1, 2, value = ProductionNames.expression.value),
            ],
            terminal_transitions=[
                TerminalTransition(1, 2, type = TokenType.KEYWORD, value = 'break'),
                TerminalTransition(2, 3, type = TokenType.SYMBOL, value = ';'),
                TerminalTransition(1, 3, type = TokenType.SYMBOL, value = ';'),
            ],
        ),
        selection_stmt = TD(
            first_node = Node(1, False, False,), 
            final_node_number = 7,
            first=[
                Pattern(type = TokenType.KEYWORD, regex = r'if'),
            ],
            follow=[
                Pattern(type = TokenType.SYMBOL, regex = r'({|}|\(|;)'),
                Pattern(type = TokenType.KEYWORD, regex = r'(break|if|repeat|return|endif|else|until)'),
                Pattern(type = TokenType.ID),
                Pattern(type = TokenType.NUM),
            ],
            non_terminal_transitions=[
                NonTerminalTransition(3, 4, value = ProductionNames.expression.value),
                NonTerminalTransition(5, 6, value = ProductionNames.statement.value),
                NonTerminalTransition(6, 7, value = ProductionNames.else_stmt.value),
            ],
            terminal_transitions=[
                TerminalTransition(1, 2, type = TokenType.KEYWORD, value = 'if'),
                TerminalTransition(2, 3, type = TokenType.SYMBOL, value = '('),
                TerminalTransition(4, 5, type = TokenType.SYMBOL, value = ')'),
            ],
        ),
        else_stmt = TD(
            first_node = Node(1, False, False,), 
            final_node_number = 4,
            first=[
                Pattern(type = TokenType.KEYWORD, regex = r'(else|endif)'),
            ],
            follow=[
                Pattern(type = TokenType.SYMBOL, regex = r'({|}|\(|;)'),
                Pattern(type = TokenType.KEYWORD, regex = r'(break|if|repeat|return|endif|else|until)'),
                Pattern(type = TokenType.ID),
                Pattern(type = TokenType.NUM),
            ],
            non_terminal_transitions=[
                NonTerminalTransition(2, 3, value = ProductionNames.statement.value),
            ],
            terminal_transitions=[
                TerminalTransition(1, 2, type = TokenType.KEYWORD, value = 'else'),
                TerminalTransition(3, 4, type = TokenType.KEYWORD, value = 'endif'),
                TerminalTransition(1, 4, type = TokenType.KEYWORD, value = 'endif'),
            ],
        ),
        iteration_stmt = TD(
            first_node = Node(1, False, False,), 
            final_node_number = 7,
            first=[
                Pattern(type = TokenType.KEYWORD, regex = r'repeat'),
            ],
            follow=[
                Pattern(type = TokenType.SYMBOL, regex = r'({|}|\(|;)'),
                Pattern(type = TokenType.KEYWORD, regex = r'(break|if|repeat|return|endif|else|until)'),
                Pattern(type = TokenType.ID),
                Pattern(type = TokenType.NUM),
            ],
            non_terminal_transitions=[
                NonTerminalTransition(2, 3, value = ProductionNames.statement.value),
                NonTerminalTransition(5, 6, value = ProductionNames.expression.value),
            ],
            terminal_transitions=[
                TerminalTransition(1, 2, type = TokenType.KEYWORD, value = 'repeat'),
                TerminalTransition(3, 4, type = TokenType.KEYWORD, value = 'until'),
                TerminalTransition(4, 5, type = TokenType.SYMBOL, value = '('),
                TerminalTransition(6, 7, type = TokenType.SYMBOL, value = ')'),
            ],
        ),
        return_stmt = TD(
            first_node = Node(1, False, False,), 
            final_node_number = 3, 
            first=[
                Pattern(type = TokenType.KEYWORD, regex = r'return'),
            ],
            follow=[
                Pattern(type = TokenType.SYMBOL, regex = r'({|}|\(|;)'),
                Pattern(type = TokenType.KEYWORD, regex = r'(break|if|repeat|return|endif|else|until)'),
                Pattern(type = TokenType.ID),
                Pattern(type = TokenType.NUM),
            ],
            non_terminal_transitions=[
                NonTerminalTransition(2, 3, value = ProductionNames.return_stmt_prime.value),
            ],
            terminal_transitions=[
                TerminalTransition(1, 2, type = TokenType.KEYWORD, value = 'return'),
            ],
        ),
        return_stmt_prime = TD(
            first_node = Node(1, False, False,), 
            final_node_number = 3, 
            first=[
                Pattern(type = TokenType.SYMBOL, regex = r'(\(|;)'),
                Pattern(type = TokenType.ID),
                Pattern(type = TokenType.NUM),
            ],
            follow=[
                Pattern(type = TokenType.SYMBOL, regex = r'({|}|\(|;)'),
                Pattern(type = TokenType.KEYWORD, regex = r'(break|if|repeat|return|endif|else|until)'),
                Pattern(type = TokenType.ID),
                Pattern(type = TokenType.NUM),
            ],
            non_terminal_transitions=[
                NonTerminalTransition(1, 2, value = ProductionNames.expression.value),
            ],
            terminal_transitions=[
                TerminalTransition(2, 3, type = TokenType.SYMBOL, value = ';'),
                TerminalTransition(1, 3, type = TokenType.SYMBOL, value = ';'),
            ],
        ),
        expression = TD(
            first_node = Node(1, False, False,), 
            final_node_number = 3, 
            first=[
                Pattern(type = TokenType.SYMBOL, regex = r'\('),
                Pattern(type = TokenType.ID),
                Pattern(type = TokenType.NUM),
            ],
            follow=[
                Pattern(type = TokenType.SYMBOL, regex = r'(;|\)|\]|,)'),
            ],
            non_terminal_transitions=[
                NonTerminalTransition(2, 3, value = ProductionNames.B.value),
                NonTerminalTransition(1, 3, value = ProductionNames.simple_expression_zegond.value),
            ],
            terminal_transitions=[
                TerminalTransition(1, 2, type = TokenType.ID),
            ],
        ),
        B = TD(
            first_node = Node(1, False, False,), 
            final_node_number = 5,
            node_size = 6,
            first=[
                EpsilonPattern(),
                Pattern(type = TokenType.SYMBOL, regex = r'(\[|=|\(|\*|\+|-|<|==)'),
            ],
            follow=[
                Pattern(type = TokenType.SYMBOL, regex = r'(;|\)|\]|,)'),
            ],
            non_terminal_transitions=[
                NonTerminalTransition(2, 3, value = ProductionNames.expression.value),
                NonTerminalTransition(4, 5, value = ProductionNames.H.value),
                NonTerminalTransition(6, 5, value = ProductionNames.expression.value),
                NonTerminalTransition(1, 5, value = ProductionNames.simple_expression_prime.value),
            ],
            terminal_transitions=[
                TerminalTransition(1, 2, type = TokenType.SYMBOL, value = '['),
                TerminalTransition(3, 4, type = TokenType.SYMBOL, value = ']'),
                TerminalTransition(1, 6, type = TokenType.SYMBOL, value = '='),
            ],
        ),
        H = TD(
            first_node = Node(1, False, False,), 
            final_node_number = 4,
            node_size = 5,
            first=[
                EpsilonPattern(),
                Pattern(type = TokenType.SYMBOL, regex = r'(=|\*|\+|-|<|==)'),
            ],
            follow=[
                Pattern(type = TokenType.SYMBOL, regex = r'(;|\)|\]|,)'),
            ],
            non_terminal_transitions=[
                NonTerminalTransition(1, 2, value = ProductionNames.G.value),
                NonTerminalTransition(2, 3, value = ProductionNames.D.value),
                NonTerminalTransition(3, 4, value = ProductionNames.C.value),
                NonTerminalTransition(5, 4, value = ProductionNames.expression.value),
            ],
            terminal_transitions=[
                TerminalTransition(1, 5, type = TokenType.SYMBOL, value = '='),
            ],
        ),
        simple_expression_zegond = TD(
            first_node = Node(1, False, False,), 
            final_node_number = 3, 
            first=[
                Pattern(type = TokenType.SYMBOL, regex = r'\('),
                Pattern(type = TokenType.NUM),
            ],
            follow=[
                Pattern(type = TokenType.SYMBOL, regex = r'(;|\)|\]|,)'),
            ],
            non_terminal_transitions=[
                NonTerminalTransition(1, 2, value = ProductionNames.additive_expression_zegond.value),
                NonTerminalTransition(2, 3, value = ProductionNames.C.value),
            ],
        ),
        simple_expression_prime = TD(
            first_node = Node(1, False, False,), 
            final_node_number = 3, 
            first=[
                EpsilonPattern(),
                Pattern(type = TokenType.SYMBOL, regex = r'(\(|\*|\+|-|<|==)'),
            ],
            follow=[
                Pattern(type = TokenType.SYMBOL, regex = r'(;|\)|\]|,)'),
            ],
            non_terminal_transitions=[
                NonTerminalTransition(1, 2, value = ProductionNames.additive_expression_prime.value),
                NonTerminalTransition(2, 3, value = ProductionNames.C.value),
            ],
        ),
        C = TD(
            first_node = Node(1, False, False,), 
            final_node_number = 3, 
            first=[
                EpsilonPattern(),
                Pattern(type = TokenType.SYMBOL, regex = r'(<|==)'),
            ],
            follow=[
                Pattern(type = TokenType.SYMBOL, regex = r'(;|\)|\]|,)'),
            ],
            non_terminal_transitions=[
                NonTerminalTransition(1, 2, value = ProductionNames.relop.value),
                NonTerminalTransition(2, 3, value = ProductionNames.additive_expression.value),
            ],
            epsilon_transitions=[
                EpsilonTransition(1, 3),
            ],
        ),
        relop = TD(
            first_node =2,
            final_node_number = 2,
            first=[
                Pattern(type = TokenType.SYMBOL, regex = r'(<|==)'),
            ],
            follow=[
                Pattern(type = TokenType.SYMBOL, regex = r'\('),
                Pattern(type = TokenType.ID),
                Pattern(type = TokenType.NUM),
            ],
            terminal_transitions=[
                TerminalTransition(1, 2, type = TokenType.SYMBOL, value = '<'),
                TerminalTransition(1, 2, type = TokenType.SYMBOL, value = '=='),
            ],
        ),
        additive_expression = TD(
            first_node = Node(1, False, False,), 
            final_node_number = 3, 
            first=[
                Pattern(type = TokenType.SYMBOL, regex = r'\('),
                Pattern(type = TokenType.ID),
                Pattern(type = TokenType.NUM),
            ],
            follow=[
                Pattern(type = TokenType.SYMBOL, regex = r'(;|\)|\]|,)'),
            ],
            non_terminal_transitions=[
                NonTerminalTransition(1, 2, value = ProductionNames.term.value),
                NonTerminalTransition(2, 3, value = ProductionNames.D.value),
            ],
        ),
        additive_expression_prime = TD(
            first_node = Node(1, False, False,), 
            final_node_number = 3, 
            first=[
                EpsilonPattern(),
                Pattern(type = TokenType.SYMBOL, regex = r'(\(|\*|\+|-)'),
            ],
            follow=[
                Pattern(type = TokenType.SYMBOL, regex = r'(<|==|;|\)|\]|,)'),
            ],
            non_terminal_transitions=[
                NonTerminalTransition(1, 2, value = ProductionNames.term_prime.value),
                NonTerminalTransition(2, 3, value = ProductionNames.D.value),
            ],
        ),
        additive_expression_zegond = TD(
            first_node = Node(1, False, False,), 
            final_node_number = 3, 
            first=[
                Pattern(type = TokenType.SYMBOL, regex = r'\('),
                Pattern(type = TokenType.NUM),
            ],
            follow=[
                Pattern(type = TokenType.SYMBOL, regex = r'(<|==|;|\)|\]|,)'),
            ],
            non_terminal_transitions=[
                NonTerminalTransition(1, 2, value = ProductionNames.term_zegond.value),
                NonTerminalTransition(2, 3, value = ProductionNames.D.value),
            ],
        ),
        D = TD(
            first_node = Node(1, False, False,), 
            final_node_number = 4,
            first=[
                EpsilonPattern(),
                Pattern(type = TokenType.SYMBOL, regex = r'(\+|-)'),
            ],
            follow=[
                Pattern(type = TokenType.SYMBOL, regex = r'(<|==|;|\)|\]|,)'),
            ],
            non_terminal_transitions=[
                NonTerminalTransition(1, 2, value = ProductionNames.addop.value),
                NonTerminalTransition(2, 3, value = ProductionNames.term.value),
                NonTerminalTransition(3, 4, value = ProductionNames.D.value),
            ],
            epsilon_transitions=[
                EpsilonTransition(1, 4),
            ],
        ),
        addop = TD(
            first_node = Node(1, False, False,), 
            final_node_number = 2,
            first=[
                Pattern(type = TokenType.SYMBOL, regex = r'(\+|-)'),
            ],
            follow=[
                Pattern(type = TokenType.SYMBOL, regex = r'\('),
                Pattern(type = TokenType.ID),
                Pattern(type = TokenType.NUM),
            ],
            terminal_transitions=[
                TerminalTransition(1, 2, type = TokenType.SYMBOL, value = '+'),
                TerminalTransition(1, 2, type = TokenType.SYMBOL, value = '-'),
            ],
        ),
        term = TD(
            first_node = Node(1, False, False,), 
            final_node_number = 3, 
            first=[
                Pattern(type = TokenType.SYMBOL, regex = r'\('),
                Pattern(type = TokenType.ID),
                Pattern(type = TokenType.NUM),
            ],
            follow=[
                Pattern(type = TokenType.SYMBOL, regex = r'(\+|-|;|\)|<|==|\]|,)'),
            ],
            non_terminal_transitions=[
                NonTerminalTransition(1, 2, value = ProductionNames.factor.value),
                NonTerminalTransition(2, 3, value = ProductionNames.G.value),
            ],
        ),
        term_prime = TD(
            first_node = Node(1, False, False,), 
            final_node_number = 3, 
            first=[
                EpsilonPattern(),
                Pattern(type = TokenType.SYMBOL, regex = r'(\*|\()'),
            ],
            follow=[
                Pattern(type = TokenType.SYMBOL, regex = r'(\+|-|;|\)|<|==|\]|,)'),
            ],
            non_terminal_transitions=[
                NonTerminalTransition(1, 2, value = ProductionNames.factor_prime.value),
                NonTerminalTransition(2, 3, value = ProductionNames.G.value),
            ],
        ),
        term_zegond = TD(
            first_node = Node(1, False, False,), 
            final_node_number = 3, 
            first=[
                Pattern(type = TokenType.SYMBOL, regex = r'\('),
                Pattern(type = TokenType.NUM),
            ],
            follow=[
                Pattern(type = TokenType.SYMBOL, regex = r'(\+|-|;|\)|<|==|\]|,)'),
            ],
            non_terminal_transitions=[
                NonTerminalTransition(1, 2, value = ProductionNames.factor_zegond.value),
                NonTerminalTransition(2, 3, value = ProductionNames.G.value),
            ],
        ),
        G = TD(
            first_node = Node(1, False, False,), 
            final_node_number = 4,
            first=[
                EpsilonPattern(),
                Pattern(type = TokenType.SYMBOL, regex = r'\*'),
            ],
            follow=[
                Pattern(type = TokenType.SYMBOL, regex = r'(\+|-|;|\)|<|==|\]|,)'),
            ],
            non_terminal_transitions=[
                NonTerminalTransition(2, 3, value = ProductionNames.factor.value),
                NonTerminalTransition(3, 4, value = ProductionNames.G.value),
            ],
            terminal_transitions=[
                TerminalTransition(1, 2, type = TokenType.SYMBOL, value = '*'),
            ],
            epsilon_transitions=[
                EpsilonTransition(1, 4),
            ],
        ),
        factor = TD(
            first_node = Node(1, False, False,), 
            final_node_number = 4,
            node_size = 5,
            first=[
                Pattern(type = TokenType.SYMBOL, regex = r'\('),
                Pattern(type = TokenType.ID),
                Pattern(type = TokenType.NUM),
            ],
            follow=[
                Pattern(type = TokenType.SYMBOL, regex = r'(\+|-|;|\)|<|==|\]|,|\*)'),
            ],
            non_terminal_transitions=[
                NonTerminalTransition(2, 3, value = ProductionNames.expression.value),
                NonTerminalTransition(5, 4, value = ProductionNames.var_call_prime.value),
            ],
            terminal_transitions=[
                TerminalTransition(1, 2, type = TokenType.SYMBOL, value = '('),
                TerminalTransition(3, 4, type = TokenType.SYMBOL, value = ')'),
                TerminalTransition(1, 5, type = TokenType.ID),
                TerminalTransition(1, 4, type = TokenType.NUM),
            ],
        ),
        var_call_prime = TD(
            first_node = Node(1, False, False,), 
            final_node_number = 4,
            first=[
                EpsilonPattern(),
                Pattern(type = TokenType.SYMBOL, regex = r'(\(|\[)'),
            ],
            follow=[
                Pattern(type = TokenType.SYMBOL, regex = r'(\+|-|;|\)|<|==|\]|,|\*)'),
            ],
            non_terminal_transitions=[
                NonTerminalTransition(2, 3, value = ProductionNames.args.value),
                NonTerminalTransition(1, 4, value = ProductionNames.var_prime.value),
            ],
            terminal_transitions=[
                TerminalTransition(1, 2, type = TokenType.SYMBOL, value = '('),
                TerminalTransition(3, 4, type = TokenType.SYMBOL, value = ')'),
            ],
        ),
        var_prime = TD(
            first_node = Node(1, False, False,), 
            final_node_number = 4,
            first=[
                EpsilonPattern(),
                Pattern(type = TokenType.SYMBOL, regex = r'\['),
            ],
            follow=[
                Pattern(type = TokenType.SYMBOL, regex = r'(\+|-|;|\)|<|==|\]|,|\*)'),
            ],
            non_terminal_transitions=[
                NonTerminalTransition(2, 3, value = ProductionNames.expression.value),
            ],
            terminal_transitions=[
                TerminalTransition(1, 2, type = TokenType.SYMBOL, value = '['),
                TerminalTransition(3, 4, type = TokenType.SYMBOL, value = ']'),
            ],
            epsilon_transitions=[
                EpsilonTransition(1, 4),
            ],
        ),
        factor_prime = TD(
            first_node = Node(1, False, False,), 
            final_node_number = 4,
            first=[
                EpsilonPattern(),
                Pattern(type = TokenType.SYMBOL, regex = r'\('),
            ],
            follow=[
                Pattern(type = TokenType.SYMBOL, regex = r'(\+|-|;|\)|<|==|\]|,|\*)'),
            ],
            non_terminal_transitions=[
                NonTerminalTransition(2, 3, value = ProductionNames.args.value),
            ],
            terminal_transitions=[
                TerminalTransition(1, 2, type = TokenType.SYMBOL, value = '('),
                TerminalTransition(3, 4, type = TokenType.SYMBOL, value = ')'),
            ],
            epsilon_transitions=[
                EpsilonTransition(1, 4),
            ],
        ),
        factor_zegond = TD(
            first_node = Node(1, False, False,), 
            final_node_number = 4,
            first=[
                Pattern(type = TokenType.SYMBOL, regex = r'\('),
                Pattern(type = TokenType.NUM),
            ],
            follow=[
                Pattern(type = TokenType.SYMBOL, regex = r'(\+|-|;|\)|<|==|\]|,|\*)'),
            ],
            non_terminal_transitions=[
                NonTerminalTransition(2, 3, value = ProductionNames.expression.value),
            ],
            terminal_transitions=[
                TerminalTransition(1, 2, type = TokenType.SYMBOL, value = '('),
                TerminalTransition(3, 4, type = TokenType.SYMBOL, value = ')'),
                TerminalTransition(1, 4, type = TokenType.NUM),
            ],
        ),
        args = TD(
            first_node = Node(1, False, False,), 
            final_node_number = 2,
            first=[
                EpsilonPattern(),
                Pattern(type = TokenType.SYMBOL, regex = r'\('),
                Pattern(type = TokenType.ID),
                Pattern(type = TokenType.NUM),
            ],
            follow=[
                Pattern(type = TokenType.SYMBOL, regex = r'\)'),
            ],
            non_terminal_transitions=[
                NonTerminalTransition(1, 2, value = ProductionNames.arg_list.value),
            ],
            epsilon_transitions=[
                EpsilonTransition(1, 2),
            ],
        ),
        arg_list = TD(
            first_node = Node(1, False, False,), 
            final_node_number = 3, 
            first=[
                Pattern(type = TokenType.SYMBOL, regex = r'\('),
                Pattern(type = TokenType.ID),
                Pattern(type = TokenType.NUM),
            ],
            follow=[
                Pattern(type = TokenType.SYMBOL, regex = r'\)'),
            ],
            non_terminal_transitions=[
                NonTerminalTransition(1, 2, value = ProductionNames.expression.value),
                NonTerminalTransition(2, 3, value = ProductionNames.arg_list_prime.value),
            ],
        ),
        arg_list_prime = TD(
            first_node = Node(1, False, False,), 
            final_node_number = 4,
            first=[
                EpsilonPattern(),
                Pattern(type = TokenType.SYMBOL, regex = r','),
            ],
            follow=[
                Pattern(type = TokenType.SYMBOL, regex = r'\)'),
            ],
            non_terminal_transitions=[
                NonTerminalTransition(2, 3, value = ProductionNames.expression.value),
                NonTerminalTransition(3, 4, value = ProductionNames.arg_list_prime.value),
            ],
            terminal_transitions=[
                TerminalTransition(1, 2, type = TokenType.SYMBOL, value = ','),
            ],
            epsilon_transitions=[
                EpsilonTransition(1, 4),
            ],
        ),
    )

    for td in info_dict.values():
        for transition in TD(td).terminal_transitions


    return td


# creating DFA

def create_dfa():
    firstState = State(1, False)
    dfa = DFA(firstState)
    # dfa.add_new_state(1, False)
    dfa.add_new_state(2, True, False, "Error", "Invalid input")
    dfa.add_new_state(3, False, False)
    dfa.add_new_state(4, False, False)
    dfa.add_new_state(5, True, False, "COMMENT")
    dfa.add_new_state(6, True, False, "NUM")
    dfa.add_new_state(7, True, False, "ID")
    dfa.add_new_state(8, True, False, "WHITESPACE")
    dfa.add_new_state(9, True, False, "SYMBOL")
    dfa.add_new_state(10, True, False, "SYMBOL")
    dfa.add_new_state(11, True, False, "SYMBOL")
    dfa.add_new_state(12, True, True, "Error", "Unmatched comment")
    dfa.add_new_state(13, True, True, "Error", "Invalid number")
    dfa.add_new_state(14, True, True, "Error", "Invalid input")
    # dfa.add_new_state(15, True, True, "Error", "Invalid input")

    dfa.add_new_transition(1, 2, regex = r'/')
    dfa.add_new_transition(2, 3, regex = r'\*')
    dfa.add_new_transition(3, 4, regex = r'\*')
    dfa.add_new_transition(3, 3, regex = r'[^\*]')
    dfa.add_new_transition(4, 3, regex = r'[^\*/]')
    dfa.add_new_transition(4, 5, regex = r'/')
    dfa.add_new_transition(4, 4, regex = r'\*')
    dfa.add_new_transition(1, 7, regex = r'[a-zA-Z]')
    dfa.add_new_transition(7, 7, regex = r'[a-zA-Z0-9]')
    dfa.add_new_transition(1, 6, regex = r'[0-9]')
    dfa.add_new_transition(6, 6, regex = r'[0-9]')
    dfa.add_new_transition(1, 8, regex = r'\s')
    # dfa.add_new_transition(8, 8, regex = r'\s')
    dfa.add_new_transition(1, 10, regex = r'=')
    dfa.add_new_transition(10, 9, regex = r'=')
    dfa.add_new_transition(1, 9, regex = r'[\;\:,\[\]\{\}\(\)\+\-\<]')

    # Errors:
    # unmatched comment error:
    dfa.add_new_transition(1, 11, regex = r'\*')
    dfa.add_new_transition(11, 12, regex = r'/')  # state 12 has error massage

    # invalid number:
    dfa.add_new_transition(6, 13, regex = r'([a-zA-Z]|[^a-zA-Z0-9;:,\[\]\(\)\{\}\+\-<=\*/\s])')
    # state 13 has error massage

    # invalid input =    state 14 has error massage
    dfa.add_new_transition(1, 14, INVALID_INPUT)
    dfa.add_new_transition(2, 14, INVALID_INPUT)
    dfa.add_new_transition(10, 14, INVALID_INPUT)
    dfa.add_new_transition(11, 14, INVALID_INPUT)
    dfa.add_new_transition(7, 14, INVALID_INPUT)

    return dfa


# creating scanner
scanner = Scanner(input_text=input_lines_string, dfa=create_dfa())

# opening output text files
tokens_file = open("tokens.txt", "w")
symbol_table_file = open("symbol_table.txt", "w")
lexical_errors_file = open("lexical_errors.txt", "w")
# reading whole text file for scanner
while not scanner.is_arrived_eof():
    lineNo, token_type, token_string, massage = scanner.get_next_token()
    # print(f"token_type, token_string = {(token_type, token_string)}")

    if len(tokens_list) != scanner.scanning_line:
        tokens_list.append([])
    if token_type not in ["WHITESPACE", "COMMENT", "Error"]:
        tokens_list[scanner.scanning_line - 1].append((token_type, token_string))
        if token_type == "ID" and token_string not in symbol_table_list:
            symbol_table_list.append(token_string)
    if token_type == "Error":
        if str(scanner.scanning_line) not in lexical_errors_list.keys():
            lexical_errors_list[str(scanner.scanning_line)] = ""
        lexical_errors_list[str(scanner.scanning_line)] += f"{(token_string, massage)} "
# symbol_table_list = list(set(symbol_table_list))
# putting lists into text files
for line, tokens in enumerate(tokens_list):
    if len(tokens) != 0:
        tokens_file.write(f"{line + 1}.   ")
        for token in tokens:
            tokens_file.write(" " + str(token))
        tokens_file.write("\n")

for line, symbol in enumerate(symbol_table_list):
    symbol_table_file.write(f"{line + 1}.\t")
    symbol_table_file.write(symbol + "\n")
if len(lexical_errors_list) == 0:
    lexical_errors_file.write("There is no lexical error.")
else:
    for key, value in lexical_errors_list.items():
        lexical_errors_file.write(f"{key}.\t{value}\n")
input_file.close()
tokens_file.close()
symbol_table_file.close()
lexical_errors_file.close()
