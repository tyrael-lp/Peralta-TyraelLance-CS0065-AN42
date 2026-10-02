import agentpy as ap
import random
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# -------- Get user input from console --------
num_agents = int(input("Enter number of agents: "))
grid_size = int(input("Enter grid size (e.g., 10 for 10x10): "))
num_steps = int(input("Enter number of steps: "))

# -------- Agent Definition -----------
class RandomWalker(ap.Agent):
    def step(self, occupied):
        direction = random.choice([(1,0), (-1,0), (0,1), (0,-1)])

        current = self.position
        x, y = self.position

        # Keep agents inside grid
        x = max(0, min(self.model.p.grid_size[0]-1, x + direction[0]))
        y = max(0, min(self.model.p.grid_size[1]-1, y + direction[1]))

        next_pos = x,y

        # If theres the space is occupied agent doesn't move
        if next_pos not in occupied:
            if current in occupied:
                occupied.remove(current) 
            
            occupied.add(next_pos)
            self.position = next_pos

# -------- Model Definition -----------
class RandomWalkModel(ap.Model):
    def setup(self):
        self.current_step = 0

        # Create agents
        self.agents = ap.AgentList(self, self.p.agents, RandomWalker)
    
        all_positions = [
            (x, y)
            for x in range(self.p.grid_size[0])
            for y in range(self.p.grid_size[1])
            ]
    
        starting_positions = random.sample(
                all_positions,
                len(self.agents)
        )

        for agent, position in zip(self.agents, starting_positions):
            agent.position = position

        # Create grid (optional)
        self.grid = ap.Grid(self, self.p.grid_size, torus=False)

        print(f"\n--- Initial Setup (Step 0) ---")
        for agent in self.agents:
            print(f"Agent {agent.id}: {agent.position}")

    def step(self):
        self.current_step += 1
        occupied = {agent.position for agent in self.agents}

        for agent in self.agents:
            agent.step(occupied)

        print(f"\n--- Step {self.current_step} ---")
        for agent in self.agents:
            print(f"Agent {agent.id}: {agent.position}")

# -------- Parameters from user input -----------
parameters = {
    'agents': num_agents,
    'grid_size': (grid_size, grid_size),
    'steps': num_steps
}

# -------- Run Model -----------
model = RandomWalkModel(parameters)
model.setup()

# -------- Interactive Animation -----------
fig, ax = plt.subplots()
ax.set_xlim(0, model.p.grid_size[0])
ax.set_ylim(0, model.p.grid_size[1])
ax.set_xticks(range(model.p.grid_size[0]+1))
ax.set_yticks(range(model.p.grid_size[1]+1))
ax.grid(True)

scat = ax.scatter([], [], s=200)  # s = size of agents

def update(frame):
    model.step()
    x = [agent.position[0] for agent in model.agents]
    y = [agent.position[1] for agent in model.agents]
    scat.set_offsets(list(zip(x, y)))
    return scat,

ani = animation.FuncAnimation(fig, update, frames=model.p.steps, blit=True, repeat=False)
plt.show()
