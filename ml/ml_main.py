from environment import LocalEnv, Cause
from agent import Agent
import numpy as np
import matplotlib.pyplot as plt
import torch
import time
import math
from cause_counter import CauseCounter

print(f"MPS Backend is available? - {"yes" if torch.backends.mps.is_available() else "no"}")

episode_count = 1000
sync_interval = 100
env = LocalEnv()
ally_agent = Agent(id="ally2")
oppoent_agent = Agent(id="opponent2")

reward_history = np.zeros(episode_count)
step_history = np.zeros(episode_count)
cause_counter = CauseCounter(buffer_size=100, episode_size=episode_count, scale=100)

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
        next_state, reward, done, cause = env.step(action)
        # if done:
        #     print(f"Episode: {episode}, Step: {step}")
        agent.update(state, action, reward, next_state, done)
        state = next_state
        total_reward += reward
        
    if episode % sync_interval == 0:
        ally_agent.sync_target()
        oppoent_agent.sync_target()
        print(f"Episode: {episode}")    
    
    reward_history[episode] = total_reward
    step_history[episode] = step
    cause_counter.append(cause, episode)


elapsed_time = time.time() - start_time
print(f"Elapsed time: {math.floor(elapsed_time / 60)}m {math.floor(elapsed_time % 60)}s ({1000 * elapsed_time / episode_count} sec/1000 episodes)")

# ally_agent.save()
# oppoent_agent.save()

# display cause history
cause_history = cause_counter.get_averages()
x = np.arange(cause_history.shape[0])
fig, ax = plt.subplots(figsize=(10, 6)) # 積み上げ棒グラフを作成
bottom = np.zeros(cause_history.shape[0]) # 最初の棒の積み上げ位置（bottom）を初期化
# 各ラベルごとに積み上げ棒を追加
for i in range(5):
    ax.bar(x, cause_history[:, i], bottom=bottom, label=Cause(i).name)
    bottom += cause_history[:, i]  # 次のラベルを積み上げる位置を更新

# display other graphs
plt.plot(reward_history, label="reward")
plt.plot(step_history, label="step")

plt.legend()
plt.show()
