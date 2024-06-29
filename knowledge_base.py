from sympy import symbols, Not, And, Or, to_cnf, Equivalent


class KnowledgeBase:
    def __init__(self):
        self.sentences = []  # Knowledge base
        self.reward = 0
        self.playerDirection = None
        self.hasArrow = True
        self.wumpusDead = False
        self.hasGold = False


    def tell(self, observation:dict, reward:float):
        x = observation['x']
        y = observation['y']

        # Add visited field to knowledge base
        self.sentences.append(symbols(f"V{x}{y}"))
        # Add if glitter is present
        if observation['glitter']:
            self.sentences.append(symbols(f"G{x}{y}"))

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
            self.sentences.append(expression_cnf)


    def ask(self, proposition):
        return self.kb.get(proposition, False)


    def pl_resolution(self, alpha):
        """
        PL-Resolution algorithm
        Args:
            alpha (str): Proposition
        Returns:
            bool: True if the proposition is true, False otherwise
        """
        clauses = self.sentences + [Not(symbols(alpha))]
        new = []
        while True:
            for i in range(len(clauses)):
                for j in range(i + 1, len(clauses)):
                    resolvents = self.pl_resolve(clauses[i], clauses[j])
                    if [] in resolvents:
                        return True
                    new += resolvents
            if set(new).issubset(set(clauses)):
                return False
            clauses += new


    def pl_resolve(self, clause1, clause2):
        """
        Resolve two clauses
        Args:
            clause1 (str): Clause 1
            clause2 (str): Clause 2
        Returns:
            list: Resolvents
        """
        resolvents = []
        for literal1 in clause1:
            for literal2 in clause2:
                if literal1 == f"¬{literal2}" or literal2 == f"¬{literal1}":
                    resolvents.append(clause1 + clause2)
        return resolvents