from environment import LocalEnv
from agent import Agent
import numpy as np
import matplotlib.pyplot as plt
import torch
import time
import math

print(f"MPS Backend is available? - {"yes" if torch.backends.mps.is_available() else "no"}")

episode_count = 200000
sync_interval = 100
env = LocalEnv()
ally_agent = Agent(id="ally")
oppoent_agent = Agent(id="opponent")

reward_history = np.zeros(episode_count)
step_history = np.zeros(episode_count)

ally_agent.load()
oppoent_agent.load()

start_time = time.time()

for episode in range(episode_count):
    state = env.reset()
    done = False
    total_reward = 0
    is_ally_turn = True
    step = 0
    
    while not done:
        step += 1
        agent = ally_agent if is_ally_turn else oppoent_agent
        action = agent.get_action(state)
        next_state, reward, done = env.step(action)
        agent.update(state, action, reward, next_state, done)
        state = next_state
        total_reward += reward
    
    if episode % sync_interval == 0:
        ally_agent.sync_target()
        oppoent_agent.sync_target()
        print(f"Episode: {episode}")
    
    reward_history[episode] = total_reward
    step_history[episode] = step


elapsed_time = time.time() - start_time
print(f"Elapsed time: {math.floor(elapsed_time / 60)}m {math.floor(elapsed_time % 60)}s ({1000 * elapsed_time / episode_count} sec/1000 episodes)")

ally_agent.save()
oppoent_agent.save()

plt.plot(reward_history, label="reward")
plt.plot(step_history, label="step")
plt.legend()
plt.show()
