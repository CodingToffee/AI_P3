from sympy import symbols, Not, And, Or, to_cnf, Equivalent


def pl_resolve(clause1, clause2):
    """
    Resolve two clauses
    Args:
        clause1 (str): Clause 1
        clause2 (str): Clause 2
    Returns:
        list: Resolvents
    """
    resolvents = []
    clause1_literals = get_literals(clause1)
    clause2_literals = get_literals(clause2)
    for literal1 in clause1_literals:
        for literal2 in clause2_literals:
            if literal1 == f"¬{literal2}" or literal2 == f"¬{literal1}":
                resolvents.append(clause1 + clause2)
    return resolvents


def get_clauses(cnf):
    if isinstance(cnf, And):
        return list(cnf.args)
    else:
        return [cnf]


def get_literals(clause):
    if isinstance(clause, Or):
        return list(clause.args)
    else:
        return [clause]


class KnowledgeBase:
    hasArrow = True
    wumpusDead = False
    hasGold = False
    def __init__(self):
        self.clauses = []  # Knowledge base
        self.reward = 0

    def tell(self, observation: dict, reward: float):
        x = observation['x']
        y = observation['y']

        # Add visited field to knowledge base
        self.clauses.append(symbols(f"V{x}{y}"))
        # Add if glitter is present
        if observation['glitter']:
            self.clauses.append(symbols(f"G{x}{y}"))

        eval = []
        if observation['breeze']:
            eval.append('B')
        if observation['stench']:
            eval.append('S')

        for e in eval:
            alpha = symbols(f"{e}{x}{y}")
            beta = []
            if x - 1 >= 0:
                beta.append(symbols(f"{e}{x - 1}{y}"))
            if x + 1 < 4:
                beta.append(symbols(f"{e}{x + 1}{y}"))
            if y - 1 >= 0:
                beta.append(symbols(f"{e}{x}{y - 1}"))
            if y + 1 < 4:
                beta.append(symbols(f"{e}{x}{y + 1}"))
            beta = And(*beta)
            expression = Equivalent(alpha, beta)
            expression_cnf = to_cnf(expression)
            self.clauses = self.clauses + get_clauses(expression_cnf)

    def ask(self, proposition):
        """
        Ask the knowledge base about a proposition
        Args:
            proposition (str): Proposition
        Returns:
            bool: True if the proposition is true, False otherwise
        """
        return self.pl_resolution(proposition)

    def pl_resolution(self, alpha):
        """
        PL-Resolution algorithm
        Args:
            alpha (str): Proposition
        Returns:
            bool: True if the proposition is true, False otherwise
        """
        clauses = self.clauses + [Not(symbols(alpha))]
        new = []
        while True:
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    resolvents = pl_resolve(clauses[i], clauses[j])
                    if [] in resolvents:
                        return True
                    new += resolvents
            if set(new).issubset(set(clauses)):
                return False
            clauses += new
