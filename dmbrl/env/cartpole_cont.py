import gym
from gym import spaces
import numpy as np

class CartPoleEnv(gym.Env):
    def __init__(self):
        # Define the parameters of the environment
        self.gravity = 9.8
        self.cart_mass = 1.0
        self.pole_mass = 0.1
        self.cart_length = 0.5
        self.total_mass = self.cart_mass + self.pole_mass
        self.pole_length = 0.8
        self.dt = 0.02  # Time step
        self.force_mag = 10.0
        
        # Define the action and observation space
        self.action_space = spaces.Box(low=-1.0, high=1.0, shape=(1,))
        self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(4,))
        
        # Set the initial state
        self.state = None
        self.reset()

    def reset(self):
        # Set the state to the unstable equilibrium position
        self.state = np.array([0.0, np.pi, 0.0, 0.0])
        return self.state
    
    def step(self, action):
        x, theta, x_dot, theta_dot = self.state

        # Clip the action to the valid range
        action = np.clip(action, self.action_space.low, self.action_space.high)

        # Calculate the force applied to the cart
        force = action[0] * self.force_mag

        # Calculate the acceleration and angular acceleration
        costheta = np.cos(theta)
        sintheta = np.sin(theta)
        temp = (force + self.pole_mass * self.pole_length * theta_dot**2 * sintheta) / self.total_mass
        theta_acc = (self.gravity * sintheta - costheta * temp) / (self.pole_length * (4.0/3.0 - self.pole_mass * costheta**2 / self.total_mass))
        x_acc = temp - self.pole_mass * self.pole_length * theta_acc * costheta / self.total_mass

        # Update the state
        x += self.dt * x_dot
        x_dot += self.dt * x_acc
        theta += self.dt * theta_dot
        theta_dot += self.dt * theta_acc

        # Wrap the angle within the range of -pi to pi
        #theta = ((theta + np.pi) % (2 * np.pi)) - np.pi
        
        # theta = self.angle_normalize(theta)

        self.state = np.array([x, theta, x_dot, theta_dot])

        # Calculate the reward (optional, you can define your own reward function here)

        # reward = np.exp(
        #     -np.sum(np.square(self._get_ee_pos(self.state) - np.array([0.0, 0.6]))) / (0.6 ** 2)
        # )
        reward = np.exp(-(1-np.cos(theta)))
        reward -= 0.01 * np.sum(np.square(action)) # Modify the reward function as per your requirement
        # costs = 10*angle_normalize(theta) ** 2 + 0.5* x**2 + 0.1 * theta_dot**2 + 1 * x_dot**2 + 0.001 * np.sum(np.square(action))
        return self.state, reward, False, {}
    
    @staticmethod
    def _get_ee_pos(x):
        x0, theta = x[0], x[1]
        return np.array([
            x0 - 0.6 * np.sin(theta),
            0.6 * np.cos(theta)
        ])
        
    @staticmethod
    def angle_normalize(x):
        return ((x + np.pi) % (2 * np.pi)) - np.pi


# """
# Classic cart-pole system implemented by Rich Sutton et al.
# Copied from http://incompleteideas.net/sutton/book/code/pole.c
# permalink: https://perma.cc/C9ZM-652R
# """
# import math
# from typing import Optional, Union

# import numpy as np

# import gym
# from gym import logger, spaces
# #from gym.envs.classic_control import utils
# from gym.error import DependencyNotInstalled


# class CartPoleEnv(gym.Env):
#     """
#     ### Description

#     This environment corresponds to the version of the cart-pole problem described by Barto, Sutton, and Anderson in
#     ["Neuronlike Adaptive Elements That Can Solve Difficult Learning Control Problem"](https://ieeexplore.ieee.org/document/6313077).
#     A pole is attached by an un-actuated joint to a cart, which moves along a frictionless track.
#     The pendulum is placed upright on the cart and the goal is to balance the pole by applying forces
#      in the left and right direction on the cart.

#     ### Action Space

#     The action is a `ndarray` with shape `(1,)` which can take values `{0, 1}` indicating the direction
#      of the fixed force the cart is pushed with.

#     | Num | Action                 |
#     |-----|------------------------|
#     | 0   | Push cart to the left  |
#     | 1   | Push cart to the right |

#     **Note**: The velocity that is reduced or increased by the applied force is not fixed and it depends on the angle
#      the pole is pointing. The center of gravity of the pole varies the amount of energy needed to move the cart underneath it

#     ### Observation Space

#     The observation is a `ndarray` with shape `(4,)` with the values corresponding to the following positions and velocities:

#     | Num | Observation           | Min                 | Max               |
#     |-----|-----------------------|---------------------|-------------------|
#     | 0   | Cart Position         | -4.8                | 4.8               |
#     | 1   | Cart Velocity         | -Inf                | Inf               |
#     | 2   | Pole Angle            | ~ -0.418 rad (-24°) | ~ 0.418 rad (24°) |
#     | 3   | Pole Angular Velocity | -Inf                | Inf               |

#     **Note:** While the ranges above denote the possible values for observation space of each element,
#         it is not reflective of the allowed values of the state space in an unterminated episode. Particularly:
#     -  The cart x-position (index 0) can be take values between `(-4.8, 4.8)`, but the episode terminates
#        if the cart leaves the `(-2.4, 2.4)` range.
#     -  The pole angle can be observed between  `(-.418, .418)` radians (or **±24°**), but the episode terminates
#        if the pole angle is not in the range `(-.2095, .2095)` (or **±12°**)

#     ### Rewards

#     Since the goal is to keep the pole upright for as long as possible, a reward of `+1` for every step taken,
#     including the termination step, is allotted. The threshold for rewards is 475 for v1.

#     ### Starting State

#     All observations are assigned a uniformly random value in `(-0.05, 0.05)`

#     ### Episode End

#     The episode ends if any one of the following occurs:

#     1. Termination: Pole Angle is greater than ±12°
#     2. Termination: Cart Position is greater than ±2.4 (center of the cart reaches the edge of the display)
#     3. Truncation: Episode length is greater than 500 (200 for v0)

#     ### Arguments

#     ```
#     gym.make('CartPole-v1')
#     ```

#     No additional arguments are currently supported.
#     """

#     metadata = {
#         "render_modes": ["human", "rgb_array"],
#         "render_fps": 50,
#     }

#     def __init__(self, render_mode: Optional[str] = None):
#         self.gravity = 9.8
#         self.masscart = 1.0
#         self.masspole = 0.1
#         self.total_mass = self.masspole + self.masscart
#         self.length = 0.5  # actually half the pole's length
#         self.polemass_length = self.masspole * self.length
#         self.force_mag = 10.0
#         self.tau = 0.02  # seconds between state updates
#         self.kinematics_integrator = "euler"

#         # Angle at which to fail the episode
#         self.theta_threshold_radians = 12 * 2 * math.pi / 360
#         self.x_threshold = 2.4

#         # Angle limit set to 2 * theta_threshold_radians so failing observation
#         # is still within bounds.
#         high = np.array(
#             [
#                 self.x_threshold * 2,
#                 np.finfo(np.float32).max,
#                 self.theta_threshold_radians * 2,
#                 np.finfo(np.float32).max,
#             ],
#             dtype=np.float32,
#         )

#         act_high = np.array((1,), dtype=np.float32)
#         self.action_space = spaces.Box(-act_high, act_high)
#         self.observation_space = spaces.Box(-high, high, dtype=np.float32)

#         self.render_mode = render_mode

#         self.screen_width = 600
#         self.screen_height = 400
#         self.screen = None
#         self.clock = None
#         self.isopen = True
#         self.state = None

#         self.steps_beyond_terminated = None

#     def step(self, action):
#         err_msg = f"{action!r} ({type(action)}) invalid"
#         #assert self.action_space.contains(action), err_msg
#         assert self.state is not None, "Call reset before using step method."
#         x, theta, x_dot, theta_dot = self.state
#         force = self.force_mag if action == 1 else -self.force_mag
#         costheta = math.cos(theta)
#         sintheta = math.sin(theta)

#         # For the interested reader:
#         # https://coneural.org/florian/papers/05_cart_pole.pdf
#         temp = (
#             force + self.polemass_length * theta_dot**2 * sintheta
#         ) / self.total_mass
#         thetaacc = (self.gravity * sintheta - costheta * temp) / (
#             self.length * (4.0 / 3.0 - self.masspole * costheta**2 / self.total_mass)
#         )
#         xacc = temp - self.polemass_length * thetaacc * costheta / self.total_mass

#         if self.kinematics_integrator == "euler":
#             x = x + self.tau * x_dot
#             x_dot = x_dot + self.tau * xacc
#             theta = theta + self.tau * theta_dot
#             theta_dot = theta_dot + self.tau * thetaacc
#         else:  # semi-implicit euler
#             x_dot = x_dot + self.tau * xacc
#             x = x + self.tau * x_dot
#             theta_dot = theta_dot + self.tau * thetaacc
#             theta = theta + self.tau * theta_dot

#         self.state = (x, theta, x_dot, theta_dot)

#         terminated = bool(
#             x < -self.x_threshold
#             or x > self.x_threshold
#             or theta < -self.theta_threshold_radians
#             or theta > self.theta_threshold_radians
#         )
        
#         # reward = np.exp(
#         #     -np.sum(np.square(self._get_ee_pos(self.state) - np.array([0.0, 0.6]))) / (0.6 ** 2)
#         # )
#         # reward -= 0.01 * np.sum(np.square(action)) # Modify the reward function as per your requirement

#         if not terminated:
#             reward = 1.0
#         elif self.steps_beyond_terminated is None:
#             # Pole just fell!
#             self.steps_beyond_terminated = 0
#             reward = 1.0
#         else:
#             if self.steps_beyond_terminated == 0:
#                 logger.warn(
#                     "You are calling 'step()' even though this "
#                     "environment has already returned terminated = True. You "
#                     "should always call 'reset()' once you receive 'terminated = "
#                     "True' -- any further steps are undefined behavior."
#                 )
#             self.steps_beyond_terminated += 1
#             reward = 0.0

#         if self.render_mode == "human":
#             self.render()
#         return np.array(self.state, dtype=np.float32), reward, terminated, {}

#     def reset(self, *, options: Optional[dict] = None):
#         # super().reset(seed=seed)
#         # Note that if you use custom reset bounds, it may lead to out-of-bound
#         # state/observations.
#         # low, high = utils.maybe_parse_reset_bounds(
#         #     options, -0.05, 0.05  # default low
#         # )  # default high
#         # high = np.array([0.05,0.05,0.05,0.05])
#         self.state = np.random.uniform(low=-0.05, high=0.05, size=(4,))
#         self.steps_beyond_terminated = None

#         if self.render_mode == "human":
#             self.render()
#         return np.array(self.state, dtype=np.float32), {}

#     def render(self):
#         if self.render_mode is None:
#             gym.logger.warn(
#                 "You are calling render method without specifying any render mode. "
#                 "You can specify the render_mode at initialization, "
#                 f'e.g. gym("{self.spec.id}", render_mode="rgb_array")'
#             )
#             return

#         try:
#             import pygame
#             from pygame import gfxdraw
#         except ImportError:
#             raise DependencyNotInstalled(
#                 "pygame is not installed, run `pip install gym[classic_control]`"
#             )

#         if self.screen is None:
#             pygame.init()
#             if self.render_mode == "human":
#                 pygame.display.init()
#                 self.screen = pygame.display.set_mode(
#                     (self.screen_width, self.screen_height)
#                 )
#             else:  # mode == "rgb_array"
#                 self.screen = pygame.Surface((self.screen_width, self.screen_height))
#         if self.clock is None:
#             self.clock = pygame.time.Clock()

#         world_width = self.x_threshold * 2
#         scale = self.screen_width / world_width
#         polewidth = 10.0
#         polelen = scale * (2 * self.length)
#         cartwidth = 50.0
#         cartheight = 30.0

#         if self.state is None:
#             return None

#         x = self.state

#         self.surf = pygame.Surface((self.screen_width, self.screen_height))
#         self.surf.fill((255, 255, 255))

#         l, r, t, b = -cartwidth / 2, cartwidth / 2, cartheight / 2, -cartheight / 2
#         axleoffset = cartheight / 4.0
#         cartx = x[0] * scale + self.screen_width / 2.0  # MIDDLE OF CART
#         carty = 100  # TOP OF CART
#         cart_coords = [(l, b), (l, t), (r, t), (r, b)]
#         cart_coords = [(c[0] + cartx, c[1] + carty) for c in cart_coords]
#         gfxdraw.aapolygon(self.surf, cart_coords, (0, 0, 0))
#         gfxdraw.filled_polygon(self.surf, cart_coords, (0, 0, 0))

#         l, r, t, b = (
#             -polewidth / 2,
#             polewidth / 2,
#             polelen - polewidth / 2,
#             -polewidth / 2,
#         )

#         pole_coords = []
#         for coord in [(l, b), (l, t), (r, t), (r, b)]:
#             coord = pygame.math.Vector2(coord).rotate_rad(-x[2])
#             coord = (coord[0] + cartx, coord[1] + carty + axleoffset)
#             pole_coords.append(coord)
#         gfxdraw.aapolygon(self.surf, pole_coords, (202, 152, 101))
#         gfxdraw.filled_polygon(self.surf, pole_coords, (202, 152, 101))

#         gfxdraw.aacircle(
#             self.surf,
#             int(cartx),
#             int(carty + axleoffset),
#             int(polewidth / 2),
#             (129, 132, 203),
#         )
#         gfxdraw.filled_circle(
#             self.surf,
#             int(cartx),
#             int(carty + axleoffset),
#             int(polewidth / 2),
#             (129, 132, 203),
#         )

#         gfxdraw.hline(self.surf, 0, self.screen_width, carty, (0, 0, 0))

#         self.surf = pygame.transform.flip(self.surf, False, True)
#         self.screen.blit(self.surf, (0, 0))
#         if self.render_mode == "human":
#             pygame.event.pump()
#             self.clock.tick(self.metadata["render_fps"])
#             pygame.display.flip()

#         elif self.render_mode == "rgb_array":
#             return np.transpose(
#                 np.array(pygame.surfarray.pixels3d(self.screen)), axes=(1, 0, 2)
#             )

#     def close(self):
#         if self.screen is not None:
#             import pygame

#             pygame.display.quit()
#             pygame.quit()
#             self.isopen = False
            

