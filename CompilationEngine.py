from JackTokenizer import *


class CompilationEngine:
    def __init__(self, input_file_path, output_path):
        self.indentation = 0
        self.input_stream = input_file_path
        self.output = output_path

    def compile_class(self):
        if self.input_stream.has_more_tokens():
            self.input_stream.advance()
            self.output.write("<class>\n")
            self.indentation += 1
            self.new_eat()
            self.input_stream.advance()
            self.new_eat()
            self.input_stream.advance()
            self.new_eat()
            self.input_stream.advance()

            while self.input_stream.current_instruction == "static" or \
                    self.input_stream.current_instruction == "field":
                self.compile_class_var_dec()
            while self.input_stream.current_instruction == "constructor" or \
                    self.input_stream.current_instruction == "function" \
                    or self.input_stream.current_instruction == "method":
                self.compile_subroutine()

            self.new_eat()
            self.indentation -= 1
            self.output.write("</class>\n")
            self.output.close()

    def compile_class_var_dec(self):
        """
        this should only print if there actually are class var decs,
        should run on the recursively
        :return:
        """
        self.output.write("  " * self.indentation + "<classVarDec>\n")
        self.indentation += 1
        self.new_eat()
        self.input_stream.advance()
        self._compile_type_and_varName()

        self.indentation -= 1
        self.output.write("  " * self.indentation + "</classVarDec>\n")

    def compile_subroutine(self):
        self.output.write("  " * self.indentation + "<subroutineDec>\n")
        self.indentation += 1
        self.new_eat()

        self.input_stream.advance()
        self.new_eat()

        self.input_stream.advance()
        self.new_eat()

        self.input_stream.advance()
        self.new_eat()

        self.input_stream.advance()
        self.compile_parameter_list()

        self.new_eat()

        self.input_stream.advance()
        # compile subroutineBody:
        self.output.write("  " * self.indentation + "<subroutineBody>\n")
        self.indentation += 1
        self.new_eat()

        self.input_stream.advance()
        while self.input_stream.current_instruction == "var":
            self.compile_var_dec()

        self.compile_statements()

        self.new_eat()
        self.indentation -= 1
        self.output.write("  " * self.indentation + "</subroutineBody>\n")
        self.indentation -= 1
        self.output.write("  " * self.indentation + "</subroutineDec>\n")
        self.input_stream.advance()

    def compile_parameter_list(self):
        self.output.write("  " * self.indentation + "<parameterList>\n")
        self.indentation += 1

        while self.input_stream.current_instruction not in POSSIBLE_SIMBOLS:
            self.new_eat()
            self.input_stream.advance()
            self.new_eat()
            self.input_stream.advance()
            if self.input_stream.symbol() == ",":
                self.new_eat()
                self.input_stream.advance()

        self.indentation -= 1
        self.output.write("  " * self.indentation + "</parameterList>\n")

    def compile_var_dec(self):
        self.output.write("  " * self.indentation + "<varDec>\n")
        self.indentation += 1

        self.new_eat()
        self.input_stream.advance()
        self._compile_type_and_varName()

        self.indentation -= 1
        self.output.write("  " * self.indentation + "</varDec>\n")

    def _compile_type_and_varName(self):
        self.new_eat()
        self.input_stream.advance()
        self.new_eat()
        self.input_stream.advance()
        while self.input_stream.current_instruction == ",":
            self.new_eat()
            self.input_stream.advance()
            self.new_eat()
            self.input_stream.advance()
        self.new_eat()
        self.input_stream.advance()

    def compile_statements(self):
        self.output.write("  " * self.indentation + "<statements>\n")
        self.indentation += 1
        self.compile_statements_body()
        self.indentation -= 1
        self.output.write("  " * self.indentation + "</statements>\n")

    def compile_statements_body(self):
        while self.input_stream.current_instruction in ['let', 'if', 'while', 'do', 'return']:
            if self.input_stream.current_instruction == 'let':
                self.compile_let()
            elif self.input_stream.current_instruction == 'if':
                self.compile_if()
            elif self.input_stream.current_instruction == 'while':
                self.compile_while()
            elif self.input_stream.current_instruction == 'do':
                self.compile_do()
            elif self.input_stream.current_instruction == 'return':
                self.compile_return()

    def compile_do(self):
        self.output.write("  " * self.indentation + "<doStatement>\n")
        self.indentation += 1

        self.new_eat()
        self.input_stream.advance()
        # subroutineCall
        self.new_eat()
        self.input_stream.advance()
        if self.input_stream.symbol() == ".":
            self.new_eat()
            self.input_stream.advance()
            self.new_eat()
            self.input_stream.advance()
        self.new_eat()
        self.input_stream.advance()
        self.compile_expression_list()
        self.new_eat()
        self.input_stream.advance()
        self.new_eat()

        self.indentation -= 1
        self.output.write("  " * self.indentation + "</doStatement>\n")
        self.input_stream.advance()

    def compile_let(self):
        self.output.write("  " * self.indentation + "<letStatement>\n")
        self.indentation += 1

        self.new_eat()
        self.input_stream.advance()
        self.new_eat()
        self.input_stream.advance()
        if self.input_stream.symbol() == "[":
            self.new_eat()
            self.input_stream.advance()
            self.compile_expression()
            self.new_eat()
            self.input_stream.advance()
        self.new_eat()
        self.input_stream.advance()
        self.compile_expression()
        self.new_eat()

        self.indentation -= 1
        self.output.write("  " * self.indentation + "</letStatement>\n")
        self.input_stream.advance()

    def compile_while(self):
        self.output.write("  " * self.indentation + "<whileStatement>\n")
        self.indentation += 1

        self.new_eat()
        self.input_stream.advance()
        self.new_eat()
        self.input_stream.advance()
        self.compile_expression()
        self.new_eat()
        self.input_stream.advance()
        self.new_eat()
        self.input_stream.advance()
        self.compile_statements()
        self.new_eat()

        self.indentation -= 1
        self.output.write("  " * self.indentation + "</whileStatement>\n")
        self.input_stream.advance()

    def compile_return(self):
        self.output.write("  " * self.indentation + "<returnStatement>\n")
        self.indentation += 1
        self.new_eat()

        self.input_stream.advance()
        if self.input_stream.current_instruction != ";":
            self.compile_expression()
        self.new_eat()

        self.indentation -= 1
        self.output.write("  " * self.indentation + "</returnStatement>\n")
        self.input_stream.advance()

    def compile_if(self):
        self.output.write("  " * self.indentation + "<ifStatement>\n")
        self.indentation += 1

        self.new_eat()
        self.input_stream.advance()

        self.new_eat()
        self.input_stream.advance()

        self.compile_expression()
        self.new_eat()

        self.input_stream.advance()
        self.new_eat()

        self.input_stream.advance()
        self.compile_statements()

        self.new_eat()
        self.input_stream.advance()

        # why we need the first condition?
        if self.input_stream.token_type() == "keyword" and \
                self.input_stream.current_instruction == "else":
            self.new_eat()
            self.input_stream.advance()

            self.new_eat()
            self.input_stream.advance()

            self.compile_statements()

            self.new_eat()
            self.input_stream.advance()

        self.indentation -= 1
        self.output.write("  " * self.indentation + "</ifStatement>\n")

    def compile_expression(self):
        """
        Note that tokenizer must be advanced before this is called!!!
        :return:
        """
        self.output.write("  " * self.indentation + "<expression>\n")
        self.indentation += 1

        self.compile_term()
        while self.input_stream.token_type() == "symbol" and \
                self.input_stream.symbol() in OP_LIST:
            self.new_eat()
            self.input_stream.advance()
            self.compile_term()

        self.indentation -= 1
        self.output.write("  " * self.indentation + "</expression>\n")

    def compile_term(self):
        self.output.write("  " * self.indentation + "<term>\n")
        self.indentation += 1
        # need to change term in here
        current_token = self.input_stream.current_instruction
        type_current_token = self.input_stream.token_type()
        self.input_stream.advance()
        if current_token in UNARY_OP:
            self.term_eat(current_token, type_current_token)
            self.compile_term()
        elif type_current_token == "identifier" and self.input_stream.current_instruction == '[':
            self.term_eat(current_token, type_current_token)
            self.new_eat()
            self.input_stream.advance()
            self.compile_expression()
            self.new_eat()
            self.input_stream.advance()
        elif type_current_token=="identifier" and self.input_stream.current_instruction == '(':
            self.term_eat(current_token, type_current_token)
            self.new_eat()
            self.input_stream.advance()
            self.compile_expression_list()
            self.new_eat()
            self.input_stream.advance()
        elif self.input_stream.current_instruction == '.':
            self.term_eat(current_token, type_current_token)
            self.new_eat()
            self.input_stream.advance()
            self.new_eat()
            self.input_stream.advance()
            self.new_eat()
            self.input_stream.advance()
            self.compile_expression_list()
            self.new_eat()
            self.input_stream.advance()
        elif current_token == '(':
            self.term_eat(current_token, type_current_token)
            self.compile_expression()
            self.new_eat()
            self.input_stream.advance()
        elif type_current_token == "identifier":
            self.term_eat(current_token, type_current_token)

        else:
            self.term_eat(current_token, type_current_token)

        self.indentation -= 1
        self.output.write("  " * self.indentation + "</term>\n")

    def term_eat(self, current_token, type_current_token):
        if current_token.startswith("\""):
            list_write = ["  " * self.indentation, "<", type_current_token, "> ", current_token[1:], " </",
                          type_current_token, ">\n"]
        else:
            list_write = ["  " * self.indentation, "<", type_current_token, "> ", current_token, " </",
                          type_current_token, ">\n"]
        for i in list_write:
            self.output.write(i)

    def compile_expression_list(self):
        self.output.write("  " * self.indentation + "<expressionList>\n")
        self.indentation += 1

        if self.input_stream.symbol() != ")":
            self.compile_expression()
            while self.input_stream.token_type() == "symbol" and \
                    self.input_stream.symbol() == ",":
                self.new_eat()
                self.input_stream.advance()
                self.compile_expression()
        if self.input_stream.symbol() == "(":
            self.compile_expression()
            while self.input_stream.token_type() == "symbol" and \
                    self.input_stream.symbol() == ",":
                self.new_eat()
                self.input_stream.advance()
                self.compile_expression()

        self.indentation -= 1
        self.output.write("  " * self.indentation + "</expressionList>\n")

    def _write_symbol(self):
        string_to_write = self.input_stream.symbol()
        if self.input_stream.symbol() == "<":
            string_to_write = "&lt;"
        elif self.input_stream.symbol() == ">":
            string_to_write = "&gt;"
        elif self.input_stream.symbol() == "&":
            string_to_write = "&amp;"
        self.output.write("  " * self.indentation + "<symbol> " +
                          string_to_write + " </symbol>\n")

    def new_eat(self):
        if self.input_stream.current_instruction in ["<", ">", "&"]:
            self._write_symbol()
            return
        elif self.input_stream.current_instruction.startswith("\""):###why?
            list_write = ["  " * self.indentation, "<", self.input_stream.token_type(), "> ",
                          self.input_stream.current_instruction[1:], " </",
                          self.input_stream.token_type(), ">\n"]
        else:
            list_write = ["  " * self.indentation, "<", self.input_stream.token_type(), "> ",
                          self.input_stream.current_instruction, " </",
                          self.input_stream.token_type(), ">\n"]
        for i in list_write:
            self.output.write(i)
