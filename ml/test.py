from environment import LocalBattlesnakeEnv

env = LocalBattlesnakeEnv(size=11, seed=1)

state = env.reset()
env.render()

actions = [0, 1, 0, 3, 2, 3, 2, 3, 2, 3, 2, 3, 2, 0, 2, 0, 0, 0]

for action in actions:
    state, reward, done = env.step(action)
    env.render()
    
    if done:
        print('Game Over')
        break

# state, reward, done = env.step(3)
# env.render()

# state, reward, done = env.step(3)
# env.render()