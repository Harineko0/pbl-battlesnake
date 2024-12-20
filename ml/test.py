from environment import LocalBattlesnakeEnv

env = LocalBattlesnakeEnv(size=11, seed=1)

state = env.reset()
env.render()

state, reward, done = env.step(0)
if done:
    print("Game Over")
    
env.render()

# state, reward, done = env.step(3)
# env.render()

# state, reward, done = env.step(3)
# env.render()