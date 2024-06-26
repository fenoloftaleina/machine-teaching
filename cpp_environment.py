import math
import gym
from gym import spaces, logger
from gym.utils import seeding
import numpy as np

class CppEnviroment(gym.Env):
    """
    Description:
        A pole is attached by an un-actuated joint to a cart, which moves along a frictionless track. The pendulum starts upright, and the goal is to prevent it from falling over by increasing and reducing the cart's velocity.
    Source:
        This environment corresponds to the version of the cart-pole problem described by Barto, Sutton, and Anderson
    Observation:
        Type: Box(4)
        Num	Observation                 Min         Max
        0	Cart Position             -4.8            4.8
        1	Cart Velocity             -Inf            Inf
        2	Pole Angle                 -24 deg        24 deg
        3	Pole Velocity At Tip      -Inf            Inf

    Actions:
        Type: Discrete(2)
        Num	Action
        0	Push cart to the left
        1	Push cart to the right

        Note: The amount the velocity that is reduced or increased is not fixed; it depends on the angle the pole is pointing. This is because the center of gravity of the pole increases the amount of energy needed to move the cart underneath it
    Reward:
        Reward is 1 for every step taken, including the termination step
    Starting State:
        All observations are assigned a uniform random value in [-0.05..0.05]
    Episode Termination:
        Pole Angle is more than 12 degrees
        Cart Position is more than 2.4 (center of the cart reaches the edge of the display)
        Episode length is greater than 200
        Solved Requirements
        Considered solved when the average reward is greater than or equal to 195.0 over 100 consecutive trials.
    """

    # metadata = {
    #     'render.modes': ['human', 'rgb_array'],
    #     'video.frames_per_second' : 50
    # }

    def __init__(self, cpp_exec_as_lib):
        self.cpp_exec_as_lib = cpp_exec_as_lib
        print(self.cpp_exec_as_lib)

        # Angle limit set to 2 * theta_threshold_radians so failing observation is still within bounds
        high = np.array([
            100.0,
            100.0
            ])

        # angle -1 or 1
        # force 0 - 36

        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(np.array([0, 0]), high, dtype=np.float32)

        self.seed()
        self.viewer = None
        self.state = None

        # self.steps_beyond_done = None

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step(self, action):
        assert self.action_space.contains(action), "%r (%s) invalid"%(action, type(action))
        state = self.state

        # game.Update();

        x, y = state
        if action == 0:
            x -= 10.0
        elif action == 1:
            x += 10.0
        elif action == 2:
            y -= 10.0
        elif action == 3:
            y += 10.0

        self.state = (x, y)

        old_x, old_y = state
        if (x < old_x or y < old_y):
            reward = 10
        else:
            reward = -20

        done = bool(x < 10.0 and y < 10.0)

        if done:
            reward = 1000

        return np.array(self.state), reward, done, {}

    def reset(self):
        self.state = self.np_random.uniform(low=0.0, high=100.0, size=(2,))
        return np.array(self.state)

    def render(self, mode='human'):
        None

    # def close(self):
