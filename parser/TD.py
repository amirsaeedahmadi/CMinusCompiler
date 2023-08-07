from enum import Enum

from scanner.DFA import TokenType

from ..scanner.scanner import Token, Scanner
from ..scanner.DFA import TokenType
from typing import Tuple 
import re


class Pattern:
    def __init__(self, regex: str, type: TokenType) -> None:
        self.regex = regex
        if self.regex is None:
            self.regex = r'.+'
        self.type = type

    def matches(self, token: Token):
        if self.type == token.type and re.match(self.regex, token.lexeme):
            return True
        return False
    
class EpsilonPattern:
    pass


class Node:
    def __init__(self, number: int, isFinal: bool = None, isError: bool = None, errorMassage: str = None):
        self.number = number
        self.isFinal = isFinal
        self.isError = isError
        self.errorMassage = errorMassage
        self.node_transitions = []
        # for a given regex check that it is available in inputs of one state transitions or not

    def __str__(self):
        return f"name : {self.name} , number : {self.number}"

    def add_new_transition(self, transition: 'TDTransition'):
        self.node_transitions.append(transition)

        

class TDTransition:
    def __init__(self, fromNode: Node, toNode: Node):
        self.fromNode = fromNode
        self.toNode = toNode

class EpsilonTransition(TDTransition):
    
    def __init__(self, from_node: Node, to_node: Node, parent_TD: 'TD') -> None:
        super().__init__(from_node, to_node)
        self.parent_TD= parent_TD

    def matches(self, token: Token) -> Tuple[Node, Token]:
        pass

class TerminalTransition(TDTransition):
    
    def __init__(self, from_node: Node, to_node: Node, parent_TD: 'TD', type: TokenType, value: str) -> None:
        super().__init__(from_node, to_node)
        self.type = type
        self.parent_TD= parent_TD
        self.value = value
        
    def matches(self, token: Token) -> Tuple[Node, Token]:
        result = None, None
        if (token.type == self.type) and (self.value == token.lexeme or self.value == None):
            result = Node(token), self.parent_TD.scanner.get_next_token()
        return result
        

class NonTerminalTransition(TDTransition):
    
    def __init__(self, from_node: Node, to_node: Node, parent_TD: 'TD', value: str) -> None:
        super().__init__(from_node, to_node)
        self.parent_TD = parent_TD

    def matches(self, token: Token) -> Tuple[Node, Token]:
        reached_final_state = False

        while(True):

            next_node, next_token = self.parent_TD.transition()
            
            if (self.toNode.isFinal):
                reached_final_state = True
                break

class ErrorType(Enum):
    TerminalMissing: 1
    NonTerminalMissing: 2
    IllegalToken: 3


class Error(Exception):
    def __init__(self, type: ErrorType) -> None:
        super().__init__()
        self.type = type
        

class TD:
    def __init__(self, first_node: Node, final_node_number: int = 0, node_size : int = 0, scanner: Scanner = None, first: list(Pattern) = None, 
                 follow: list(Pattern) = None, terminal_transitions: list(TerminalTransition) = None,
                    non_terminal_transitions: list(NonTerminalTransition) = None, 
                    epsilon_transitions: list(EpsilonTransition) = None):

        self.scanner = scanner
        self.first_node = first_node
        self.final_node = final_node_number
        self.node_size = node_size
        self.allNodes = {1: self.first_node}
        self.first = first
        self.follow = follow
        self.terminal_transitions = terminal_transitions
        self.non_terminal_transitions = non_terminal_transitions
        self.epsilon_transitions = epsilon_transitions
    

    def add_new_transition(self, fromNode: 'Node', transition: 'TDTransition'):
        self.allNodes[fromNode].add_new_transition(transition=transition)
    

    def add_new_node(self, number: int, isFinal: bool = None, isError: bool = None, 
    errorMassage: str = None):
        self.allNodes[number] = Node(number=number, isFinal=isFinal, isError=isError
        , errorMassage=errorMassage)

    def transition(self, node: 'Node', token: 'Token'):
        
        for transition in node.node_transitions:
            if transition.isinstance(TerminalTransition):         # checking for terminal transitions
                node_temp, token_temp = transition.matches(token)
                if (not node_temp is None):
                    return transition.to_node, node_temp, token_temp
            if transition.isiinstance(NonTerminalTransition):     # checking for NonTerminal transitions
                if transition.dfa.in_first(token):
                    node_temp, token_temp = transition.matches(token)
                    return transition.to_node, node_temp, token_temp
                
        epsilon_transition = next((t for t in node.node_transitions if isinstance(t, EpsilonTransition)), None)
        if epsilon_transition is None or not epsilon_transition.parent_TD.in_follow(token):
            checker = True
            for transition in node.node_transitions:              # checking that all transitions are Terminal or Epsilon
                if not isinstance(transition, TerminalTransition) and not isinstance(transition, EpsilonTransition):
                    checker = False
            
            if checker:
                # Call the error logger:missing first transition.value
                print(f'#{token.lineno}:Missing {node.node_transitions[0].value or node.node_transitions[0].type.name}')
                raise Error(ErrorType.TerminalMissing)
            
            non_terminal_transition = next((t for t in node.node_transitions if isinstance(t, NonTerminalTransition)))

            if non_terminal_transition.parent_TD.in_follow(token):
                # Call the error logger: missing self.name
                print(f'#{token.lineno}:Missing {non_terminal_transition.name}')
                raise Error(ErrorType.NonTerminalMissing)

            # Call the error logger:illegal token
            print(f'#{token.lineno}:Illegal {token.lexeme if token.type not in [TokenType.ID, TokenType.NUM] else token.type.name}')
            raise Error(ErrorType.IllegalToken)

    def in_first(self, token: Token) -> bool:
        m = self._in_set(self.first, token)
        if not m and any(isinstance(other_m, EpsilonMatchable) for other_m in self.first):
            return self.in_follow(token)
        return m

    def in_follow(self, token: Token) -> bool:
        return self._in_set(self.follow, token)

    @staticmethod
    def _in_set(the_set: Iterable[Matchable], token: Token) -> bool:
        return next((True for m in the_set if not isinstance(m, EpsilonMatchable) and m.matches(token)), False)
