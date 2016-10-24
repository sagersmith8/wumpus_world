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
        self.pos = set(pos)
        self.neg = set(neg)

    def rename_suffix(self, suffix):
        """
        Renames the suffixes of variable on all of the syntax
        nodes so that they can be distinguished from unrelated
        variables in other clauses.

        :param suffix: the suffix to add to each variable name
        :type suffix: string
        """
        for term in self.pos | self.neg:
            term.rename_suffix(suffix)

    def tautological(self):
        for pterm in self.pos:
            for nterm in self.neg:
                if node.unify(pterm, nterm) is not None:
                    return True
        return False

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
        if self.empty():
            return '[empty]'
        return ' or '.join(map(repr, self.pos)) + (' or ' if self.pos and self.neg else '') + ('not ' if self.neg else '') + ' or not '.join(map(repr, self.neg))

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

    round = 0
    while True:
        print "Resolution: Round {}".format(round)
        for clause in clauses:
            print "  " + repr(clause)        
        new = set()
        for clause_pair in itertools.combinations(clauses, 2):
            resolvents = resolve(*clause_pair)
            if resolvents:
                print "Resolved:"
                print "--{}".format(clause_pair[0])
                print "--{}".format(clause_pair[1])
                print "----"
                print '\n'.join(map(repr,resolvents))
                print ''
            for resolvent in resolvents:
                if resolvent.empty():
                    #print "Resolved {} and {} to nothing".format(*clause_pair)
                    return True
            new |= {resolvent for resolvent in resolvents if not resolvent.tautological()}
        if new <= clauses:
            return False
        #print "Resolved new clauses: {}".format(new)
        clauses |= new
        round += 1


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
    resolvent_clauses = set()

    all_pos = clause_one.pos | clause_two.pos
    all_neg = clause_one.neg | clause_two.neg

    return (resolve_with(clause_one.pos, clause_two.neg, all_pos, all_neg) |
            resolve_with(clause_two.pos, clause_one.neg, all_pos, all_neg))


def resolve_with(pos, neg, all_pos, all_neg):
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
    resolvents = set()

    for pterm in pos:
        for nterm in neg:
            subs = node.unify(pterm, nterm)

            if subs is not None:
                #print "Unified {} and {}:::{}".format(pterm, nterm, subs)
                resolvents.add(Clause(
                    (factor([substitute_term(subs, term) for term in all_pos - {pterm}])),
                    (factor([substitute_term(subs, term) for term in all_neg - {nterm}])),
                ))
                break

    return resolvents

def factor(term_list):
    for (ida, terma), (idb, termb) in itertools.combinations(enumerate(term_list), 2):
        subs = node.unify(terma, termb)
        if subs is not None:
            term_list.pop(ida)
            return factor([substitute_term(subs, term) for term in term_list])
    return term_list
            

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
