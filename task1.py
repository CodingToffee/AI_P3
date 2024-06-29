import gym
import fh_ac_ai_gym
from knowledge_base import KnowledgeBase

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
    if kb.ask("W{x}{y+1}") is False and kb.ask("P{x}{y+1}") is False:
        return x, y + 1
    if kb.ask("W{x}{y-1}") is False and kb.ask("P{x}{y-1}") is False:
        return x, y - 1
    if kb.ask("W{x+1}{y}") is False and kb.ask("P{x+1}{y}") is False:
        return x + 1, y
    if kb.ask("W{x-1}{y}") is False and kb.ask("P{x-1}{y}") is False:
        return x - 1, y
    return None

def get_action(kb: KnowledgeBase, x, y, direction):
    safe_x, safe_y = get_safe_field(kb, x, y)
    # If there is glitter, pick up the gold
    if kb.ask("G{x}{y}"):
        return "5"
    if safe_x is None:
        return "4"
    # If the safe field is in front of the player, go forward




wumpus_env = gym.make('Wumpus-v0')
obs = wumpus_env.reset()
knowledge_base = KnowledgeBase()

# Tell the knowledge base about the initial observation
knowledge_base.tell(obs, 0)
print(obs['direction'].value)
print(obs)
wumpus_env.render()

last_action = None

# done = False
# while not done:
#     # Ask the knowledge base about the next action
#     action = knowledge_base.ask("GoForward")
#     if action is None:
#         action = 0
#
#     obs, reward, done, info = wumpus_env.step(action)
#     wumpus_env.render()
#
#     # Tell the knowledge base about the observation
#     knowledge_base.tell(obs, reward)


wumpus_env.close()
