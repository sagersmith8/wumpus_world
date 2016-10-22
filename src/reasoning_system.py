import itertools
import node


class ReasoningSystem:
    def __init__(self, axioms):
        """
        Creates a new reasoning system that can store axioms and
        perform resolution to try to prove queries.

        :param axioms: the initial axioms for the system
        :type axioms: list[Clause]
        """
        self.facts = list(axioms)
        separate_apart(self.facts)

    def tell(self, fact):
        """
        Adds a fact to the knowledge base, to be used when
        proving later queries.

        :param fact: the fact to add
        :type fact: Clause
        """
        fact.rename_suffix(str(len(self.facts)))
        self.facts.append(fact)

    def ask(self, query):
        """
        Tries to prove a given query based on stored knowledge
        by applying resolution.

        :rtype: bool
        :returns: whether or not the query can be proven
        """
        return resolution(self.facts, query)


class Clause:
    def __init__(self, pos, neg):
        """
        Creates a new disjunctive clause separated into positive
        and negative terms.

        :param pos: the non-negated terms in the clause
        :type pos: list[Node]
        :param neg: the negated terms in the clause
        :type neg: list[Node]
        """
        self.pos = pos
        self.neg = neg

    def rename_suffix(self, suffix):
        """
        Renames the suffixes of variable on all of the syntax
        nodes so that they can be distinguished from unrelated
        variables in other clauses.

        :param suffix: the suffix to add to each variable name
        :type suffix: string
        """
        for term in self.pos + self.neg:
            term.rename_suffix(suffix)

    def empty(self):
        """
        Determines whether this clause is the empty clause (that
        is, whether it has no terms).

        :rtype: bool
        :returns: whether or not this clause is empty
        """
        return len(self.pos) == 0 and len(self.neg) == 0

    def __repr__(self):
        """
        Gives a simple representation of the Clause
        """
        return repr(self.pos) + " > " + repr(self.neg)

    def __eq__(self, other):
        return self.pos == other.pos and self.neg == other.neg

    def __hash__(self):
        return hash((tuple(self.pos), tuple(self.neg)))


def separate_apart(clauses):
    """
    'Separate apart' a list of caluses, ensure that variables
    coming from separate clauses don't interfere with each other
    by coincidentally sharing the same name.

    :param clauses: the clauses to separate apart
    :type clauses: list[Clause]
    """
    for index, clause in enumerate(clauses):
        clause.rename_suffix(str(index))


def substitute_term(sub_str, term):
    """
    Create a new Node by applying a substitution string over its
    entire tree structure.
    """
    for var_name in sub_str.iterkeys():
        term = term.replace(var_name, sub_str[var_name])

    return term


def resolution(clauses, query):
    """
    Tries to prove a given query by contradiction by repeatedly
    applying resolution in stages. So, first the query is assumed
    to be false.

    If a contradicion is reached, the query is proved.

    If no new clauses are found, at some point, then the query
    cannot be proved from the current knowledge base.

    :param clauses: the basic knowledge of the system
    :type clauses: list[Clause]
    :param query: the query to try to prove
    :type query: Clause
    :rtype: bool
    :returns: whether or not the query can be proved from the
        provided facts.
    """
    clauses = set(clauses)

    if query.neg and query.pos:
        return None
    
    clauses.add(Clause(query.neg, query.pos)) # negate the query

    while True:
        new = set()
        for clause_pair in itertools.combinations(clauses, 2):
            resolvents = resolve(*clause_pair)
            if resolvents:
                if resolvents.empty():
                    return True
                new |= {resolvents}
        if new <= clauses:
            return False
        clauses |= new


def resolve(clause_one, clause_two):
    """
    Resolves the two clauses, return a new clause with variables subsituted
    and disjuncts removed according to their unification.

    Specifically, if any positive disjunct unfies with a negative disjunct
    from the other clause, both are removed from the result and the substit-
    ution string is applied to the final result.

    :param clause_one: the first clause to resolve
    :type clause_one: Clause
    :param clause_two: the other clause to resolve
    :type clause_two: Clause
    :rtype: Clause
    :returns: the Clause resulting from performing resolution
    """
    sub_str = {}
    new_pos = []
    new_neg = []

    resolve_with(clause_one.pos, clause_two.neg, sub_str, new_pos, new_neg)
    resolve_with(clause_two.pos, clause_one.neg, sub_str, new_pos, new_neg)

    if len(new_neg) == len(clause_one.neg) + len(clause_two.neg):
        return None

    new_neg = [substitute_term(sub_str, term) for term in new_neg]
    new_pos = [substitute_term(sub_str, term) for term in new_pos]

    return Clause(new_pos, new_neg)


def resolve_with(pos, neg, sub_str, new_pos, new_neg):
    """
    Resolves the positive terms from one clause with the negative terms
    of another clause, updating the subsitution string and adding
    any terms that aren't resolved to the new clause.

    :param pos: the positive disjuncted terms from one clause
    :type pos: list[Node]
    :param neg: the negative disjuncted terms from the other clause
    :type neg: list[Node]
    :param sub_str: the substitution string to update
    :type sub_str: map{string: Node}
    :param new_pos: the positive disjuncted terms to be in the resulting clause
    :type new_pos: list[Node]
    :param new_pos: the negative disjuncted terms to be in the resulting clause
    :type new_neg: list[Node]
    """
    untouched_neg = set(neg)

    for pterm in pos:
        resolved_term = False
        for nterm in neg:
            nterm = substitute_term(sub_str, nterm)
            subs = node.unify(pterm, nterm)

            if subs is not None:
                pterm = substitute_term(subs, pterm)
                sub_str.update(subs)
                resolved_term = True
                untouched_neg.discard(nterm)
        if not resolved_term:
            new_pos.append(pterm)

    new_neg.extend(list(untouched_neg))


if __name__ == '__main__':
    """
    A simple test of reasoning system.

    Initial knowledge:
     -f(x) :- g(x)

    Told:
     -g(5)

    Tested:
     -can prove f(5)
     -can't prove f(4)
    """
    from node import var, func, const

    r = Clause([func('f', [var('x')])], [func('g', [var('x')])])
    rs = ReasoningSystem([r])
    rs.tell(Clause([func('g', [const(5)])], []))

    print rs.ask(Clause([func('f', [const(5)])], []))
    print rs.ask(Clause([func('f', [const(4)])], []))
