
"""
Types that AST nodes can have.
Behavior and properties are described in more detail
in the appropriate sections for building each node.
"""
ast_types = range(3)
CONST, VAR, FUNC = ast_types


class Node:
    """
    A syntax node representing at most a term in a disjunction.
    """
    def __init__(self, type, name, args=None):
        """
        Creates a normal syntax node.

        :param type: the kind of node being created
        :type type: int
        :param name: the name of the node
        :type name: string or int
        :param args: extra argument(s) needed by the node
        :type param: list[Node], int, or None (depending of node type)
        """
        self.type = type
        self.name = name
        self.args = args

    def __repr__(self):
        """
        A basic representation of a node for debugging.
        """
        return '{}:{} [{}]'.format(self.type, self.name, self.args)

    def __eq__(self, other):
        return (self.type == other.type and
                self.name == other.name and
                self.args == other.args)

    def __hash__(self):
        if type(self.args) == list:
            return hash((self.type, self.name, tuple(self.args)))
        return hash((self.type, self.name, self.args))

    def rename_suffix(self, suffix):
        """
        Recursively traverses the syntax tree to appends a suffix
        to all variable names. Mostly useful for separating clauses
        apart from each other.

        :param suffix: the suffix to add to each variable name
        :type suffix: string
        """
        if self.type == VAR:
            self.name += suffix
        if self.type == FUNC:
            for arg in self.args:
                arg.rename_suffix(suffix)

    def replace(self, var_name, node):
        """
        Constructs a new node with any variables with the given
        name in the specified node replaced with the given
        replacement node.

        :param var_name: the name of the variable to replace
        :type var_name: string
        :param node: the node to replace the specified variable
        :type node: Node
        :rtype: Node
        :returns: a node with the given variable replaced by a
            specific node.
        """
        if self.type == VAR and self.name == var_name:
            if self.args != 0:
                if node.type == VAR:
                    return var(node.name, self.args + node.args)
                if node.type == CONST:
                    return var(node.name + self.args)
                else:
                    raise Exception("Can not offset a function")
            return node
        if self.type == FUNC:
            return func(self.name, [
                arg.replace(var_name, node) for arg in self.args
            ])
        return self


def const(name):
    """
    Creates a node representing a constant.

    :param name: name or numeric value of the constant
    :type name: string or int (depending on the kind of constant)
    :rtype: Node
    :returns: a node representing the given constant
    """
    return Node(CONST, name)


def var(name, offset=0):
    """
    Creates a node representing a variable, potentially having
    an arithmetic offset.
    (e.g. var(x, offset=1) represents X+1)

    :param name: the variable's name
    :type name: string
    :param offset: the variable's arithmetic offset
    :type offset: int
    :rtype: Node
    :returns: a node reprsenting a variable
    """
    return Node(VAR, name, offset)


def func(name, args):
    """
    Creates a node representing a function call, having as
    many arguments as necessary.

    :param name: the function's name
    :type name: string
    :param args: the parameters to the function
    :type args: list[Node]
    :rtype: Node
    :returns: a node reprsenting a function call
    """
    return Node(FUNC, name, args)


def unify(node1, node2):
    """
    Unfies two syntax nodes and gives the substitution string
    which unfies the two nodes.

    :param node1: the first node to unify
    :type node1: Node
    :param node2: the second node to unify
    :type node2: Node
    :rtype: map{str: Node}
    :returns: a map from variable names to the nodes to replace
        those variables, or None if the two terms can't unify.
    """
    return unify_str(node1, node2, {})


def unify_str(node1, node2, subs):
    """
    Recursively unfies two syntax nodes having already processed
    the given substitutions.

    :param node1: the first node to unify
    :type node1: Node
    :param node2: the second node to unify
    :type node2: Node
    :rtype: map{str: Node}
    :returns: a substitution map from variable names to the nodes
        to replace those variables, or None if the two terms don't
        unify.
    """
    if node1.type == CONST and node2.type == CONST:
        if node1.name == node2.name:
            return subs
        return None
    if node1.type == VAR:
        return unify_var(node1, node2, subs)
    if node2.type == VAR:
        return unify_var(node2, node1, subs)
    if node2.type == FUNC and node2.type == FUNC:
        if node1.name != node2.name:
            return None
        if len(node1.args) != len(node2.args):
            return None

        for i in xrange(len(node1.args)):
            res = unify_str(node1.args[i], node2.args[i], subs)
            if res is None:
                return None
        return subs
    return None


def unify_var(variable, other, subs):
    """
    Recursively unfies two syntax nodes, one of which is known
    to be a variable, having already processed the given
    substitutions.

    This factors in some edge cases for variable offset arith-
    matic, and variables already being unified.

    Does not include the occurs check (but it really should).

    :param variable: the variable to unify
    :type variable: Node
    :param other: the other node to unify with
    :type other: Node
    :returns: a substitution map
    """
    if variable.name in subs:
        sub_term = subs[variable.name]
        if sub_term.type == VAR:
            return unify_str(var(
                sub_term.name, variable.args + sub_term.args
            ), other, subs)
        else:
            return unify_str(sub_term, other, subs)
    if other.type == VAR and other.name in subs:
        sub_term = subs[other.name]
        if sub_term.type == VAR:
            return unify_str(variable, var(
                sub_term.name, other.args + sub_term.args
            ), subs)
        else:
            return unify_str(sub_term, other, subs)
    if variable.args != 0:
        if other.type == CONST:
            if type(other.name) != int:
                return None
            subs[variable.name] = const(other.name - variable.args)
            return subs
        elif other.type == FUNC:
            return None

    if other.type == VAR:
        subs[variable.name] = var(other.name, other.args - variable.args)
        subs[other.name] = var(variable.name, variable.args - other.args)
    else:
        subs[variable.name] = other
    return subs
