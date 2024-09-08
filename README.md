# mparena
`mparena` is a example of using the `multiprocessing` library to simulate thousands of agents (the `Player` class) simultaneously by making full use of all CPU cores.

The advantage of multiprocessing can be seen when simulating more than 1000 agents. 

## `unshared.py`
This method is the faster implementation, but the drawback is that it is incapable of ensuring all agents work with every other agent, as agents are split into chunks which can only interact with agents of each chunk.

## `shared.py`
This method is the much slower implementation, but has the advantage of allowing all agents to work with any other agent within the same `Arena`.

## Usage
```bash
python unshared.py
# OR
python shared.py
```
