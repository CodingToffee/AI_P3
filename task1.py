import gym
import fh_ac_ai_gym
from knowledge_base import KnowledgeBase
from sympy import symbols

def test_knowledge_base(kb):
    A = symbols('A')
    B = symbols('B')
    C = symbols('C')


def get_direction(observation):
    """
    Converts the direction to NORTH, SOUTH, EAST, WEST
    Args:
        direction (str): Direction
    Returns:
        str: NORTH, SOUTH, EAST, WEST
    """
    if observation['direction'].value == 0:
        return 'NORTH'
    if observation['direction'].value == 1:
        return 'EAST'
    if observation['direction'].value == 2:
        return 'SOUTH'
    if observation['direction'].value == 3:
        return 'WEST'


def get_turn_direction(current_direction, current_x, current_y, new_x, new_y):
    """
    Get the turn direction
    Args:
        current_direction (str): Current direction
        current_x (int): Current x coordinate
        current_y (int): Current y coordinate
        new_x (int): New x coordinate
        new_y (int): New y coordinate
    Returns:
        str: Turn direction
    """
    if current_x == new_x:
        if current_y > new_y:
            if current_direction == 'NORTH' or current_direction == 'EAST':
                # Turn right
                return 2
            elif current_direction == 'WEST':
                # Turn left
                return 1
            elif current_direction == 'SOUTH':
                # Walk
                return 0
        elif current_y < new_y:
            if current_direction == 'SOUTH' or current_direction == 'WEST':
                # Turn right
                return 2
            elif current_direction == 'EAST':
                # Turn left
                return 1
            elif current_direction == 'NORTH':
                # Walk
                return 0
    if current_y == new_y:
        if current_x > new_x:
            if current_direction == 'SOUTH' or current_direction == 'EAST':
                # Turn right
                return 2
            elif current_direction == 'NORTH':
                # Turn left
                return 1
            elif current_direction == 'WEST':
                # Walk
                return 0
        elif current_x < new_x:
            if current_direction == 'NORTH' or current_direction == 'WEST':
                # Turn right
                return 2
            elif current_direction == 'SOUTH':
                # Turn left
                return 1
            elif current_direction == 'EAST':
                # Walk
                return 0
    return None


def get_safe_field(kb: KnowledgeBase, x, y):
    """
    Checks on which field there is no Wumpus nor a Pit
    Args:
        kb (KnowledgeBase): Knowledge base
        x (int): x coordinate
        y (int): y coordinate
    Returns:
        (x, y) (tuple): Coordinates of the safe field
    """
    if KnowledgeBase.hasArrow:
        if y + 1 <= 3:
            if kb.ask("W{x}{y+1}") is False and kb.ask("P{x}{y+1}") is False and kb.ask("V{x}{y+1}") is False:
                return x, y + 1
        if y - 1 >= 0:
            if kb.ask("W{x}{y-1}") is False and kb.ask("P{x}{y-1}") is False and kb.ask("V{x}{y-1}") is False:
                return x, y - 1
        if x + 1 <= 3:
            if kb.ask("W{x+1}{y}") is False and kb.ask("P{x+1}{y}") is False and kb.ask("V{x+1}{y}") is False:
                return x + 1, y
        if x - 1 >= 0:
            if kb.ask("W{x-1}{y}") is False and kb.ask("P{x-1}{y}") is False and kb.ask("V{x-1}{y}") is False:
                return x - 1, y
        return None
    else:
        if y + 1 <= 3:
            if (kb.ask("W{x}{y+1}") is False or kb.ask("P{x}{y+1}") is False) and kb.ask("V{x}{y+1}") is False:
                return x, y + 1
        if y - 1 >= 0:
            if (kb.ask("W{x}{y-1}") is False or kb.ask("P{x}{y-1}") is False) and kb.ask("V{x}{y-1}") is False:
                return x, y - 1
        if x + 1 <= 3:
            if (kb.ask("W{x+1}{y}") is False or kb.ask("P{x+1}{y}") is False) and kb.ask("V{x+1}{y}") is False:
                return x + 1, y
        if x - 1 >= 0:
            if (kb.ask("W{x-1}{y}") is False or kb.ask("P{x-1}{y}") is False) and kb.ask("V{x-1}{y}") is False:
                return x - 1, y
        return None


def get_action(kb: KnowledgeBase, x, y, direction):
    print("Current position:", x, y)
    safe_x, safe_y = get_safe_field(kb, x, y)
    print("Safe field:", safe_x, safe_y)
    print("Knowledge: ", kb.clauses)
    if safe_x is not None:
        print("Safe Field Visited: ", kb.ask(f"V{safe_x}{safe_y}"))
    # If there is glitter, pick up the gold
    if kb.ask("G{x}{y}"):
        return "5"
    if safe_x is None and KnowledgeBase.hasArrow:
        # Shoot the arrow
        KnowledgeBase.hasArrow = False
        return "4"
    # If the safe field is in front of the player, go forward
    turn_direction = get_turn_direction(direction, x, y, safe_x, safe_y)
    print("Turn direction:", turn_direction)
    return turn_direction


wumpus_env = gym.make('Wumpus-v0')
obs = wumpus_env.reset()
knowledge_base = KnowledgeBase()

# Tell the knowledge base about the initial observation
knowledge_base.tell(obs, 0)
print("Current position:", obs['x'], obs['y'])
print("Knowledge:", knowledge_base.clauses)
print("W01", knowledge_base.ask("W01"))
direction = get_direction(obs)
wumpus_env.render()

last_action = None

# done = False
# while not done:
#     # Get the action from the knowledge base
#     action = get_action(knowledge_base, obs['x'], obs['y'], direction)
#     print("Action:", action)
#
#     obs, reward, done, info = wumpus_env.step(action)
#     wumpus_env.render()
#
#     direction = get_direction(obs)
#
#     # Tell the knowledge base about the observation
#     knowledge_base.tell(obs, reward)
#
#
# wumpus_env.close()
