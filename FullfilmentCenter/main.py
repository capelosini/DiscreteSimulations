import simpy


def wait(env, duration):
    print(env.now, "Waiting...")
    yield env.timeout(duration)


env = simpy.Environment()

env.process(wait(env, 3))

env.run(until=10)
