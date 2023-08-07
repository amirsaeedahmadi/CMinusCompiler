import re
from .DFA import TokenType

class Scanner:

    def __init__(self, dfa, input_text=None, ):
        self.scanning_line = 1
        self.scanning_char = 0
        self.starting_char = 0
        self.current_i = 0
        self.dfa = dfa
        self.input_text = input_text

    def panic_mode(self):
        pass

    def get_next_token(self):
        # print(f"all states : {self.dfa.allStates}")
        keyword_name = "ID"
        current_state = self.dfa.firstState
        # print(f"first_state.state_transitions : {current_state.state_transitions}")
        # print(f"first_state: {current_state}")

        # for self.scanning_char, character in enumerate(self.input_text):
        for i in range(self.starting_char, len(self.input_text)):

            self.scanning_char = i
            character = self.input_text[i]
            if character == "\n" and (self.starting_char == i):
                self.change_scanning_line(i)
            next_state = None
            no_transition = True
            for transition in current_state.state_transitions:
                # print(f"transition state : {transition.toState}")

                if re.match(transition.regex, character):
                    no_transition = False
                    next_state = transition.toState
                    current_state = next_state
                    break

            if not no_transition:
                continue
            if next_state == None:
                if current_state.isFinal:
                    token_string = self.input_text[self.starting_char:self.scanning_char]
                    if current_state.name == "ID":
                        if token_string in keywords:
                            keyword_name = "KEYWORD"
                    else:
                        keyword_name = current_state.name
                    self.starting_char = self.scanning_char
                    massage = ""
                    if keyword_name == "Error":
                        massage = current_state.errorMassage
                    return self.scanning_line, keyword_name, token_string, massage,
            else:
                return self.scanning_line, "", "", ""

        if self.is_arrived_eof():
            length = self.scanning_char - self.starting_char + 1
            error_comment = ""
            temp = self.input_text[self.starting_char : self.starting_char + 2]
            if (self.input_text[self.starting_char : self.starting_char + 2] == "/*"):

                if length > 7:
                    error_comment += self.input_text[self.starting_char:self.starting_char + 7] + "..."
                else:
                    error_comment += self.input_text[self.starting_char: length + 1]
                return self.scanning_line, "Error", error_comment, "Unclosed comment"
            else:
                if current_state.isFinal:
                    token_string = self.input_text[self.starting_char:self.scanning_char + 1]
                    if current_state.name == "ID":
                        if token_string in keywords:
                            keyword_name = "KEYWORD"
                    else:
                        keyword_name = current_state.name
                    self.starting_char = self.scanning_char
                    massage = ""
                    if keyword_name == "Error":
                        massage = current_state.errorMassage
                    return self.scanning_line, keyword_name, token_string, massage,

    def change_scanning_line(self, i):
        if i != self.current_i:
            self.current_i = i
            self.scanning_line += 1

    def is_arrived_eof(self):
        some = len(self.input_text)
        if self.scanning_char < (len(self.input_text) - 1):
            return False
        return True


keywords = ["if", "else", "void", "int", "endif" "repeat", "until", "break", "return"]

    
class Token:
    def __init__(self, type: TokenType, lexeme: str, lineno: int):
        self.type = type
        self.lexeme = lexeme
        self.lineno = lineno
    
    def __repr__(self) -> str:
        return f'({self.type}, {self.lexeme})'
