# RVO
"""
La velocidad es un vector en el algoritmo RVO porque la velocidad de un agente no solo tiene una magnitud (la velocidad en sí misma), sino 
también una dirección en la que se está moviendo. En una simulación de comportamiento de agentes, es común representar la velocidad como un 
vector que describe tanto la magnitud como la dirección del movimiento.

En el algoritmo RVO, los agentes interactúan entre sí al tomar en cuenta sus velocidades relativas. Para poder hacer esto, la velocidad se 
representa como un vector. De esta manera, se puede calcular el ángulo entre las velocidades de dos agentes y tomar decisiones basadas en esa 
información. Además, el vector velocidad también es importante para calcular la distancia que recorrerá un agente en un período de tiempo 
determinado.

En resumen, la velocidad se representa como un vector en el algoritmo RVO porque es una cantidad que tiene tanto una magnitud como una 
dirección, y es necesaria para calcular las interacciones entre agentes en una simulación.
"""

import math

class Agent:
    def __init__(self, position, velocity, goal):
        self.position = position
        self.velocity = velocity
        self.goal = goal
    
    def compute_new_velocity(self, agents):
        # Calculate preferred velocity towards the goal
        preferred_velocity = self.goal - self.position
        preferred_velocity = normalize(preferred_velocity) * max_speed
        
        # Compute the reciprocal velocity obstacle (RVO) for all other agents
        obstacle_velocities = []
        for agent in agents:
            if agent != self:
                relative_position = agent.position - self.position
                relative_velocity = self.velocity - agent.velocity
                distance = math.sqrt(relative_position.dot(relative_position))
                time_to_collision = -relative_position.dot(relative_velocity) / (relative_velocity.dot(relative_velocity) + 0.0001)
                if time_to_collision > 0 and time_to_collision < time_horizon:
                    obstacle_velocity = -normalize(relative_position + relative_velocity * time_to_collision) * max_speed
                    obstacle_velocities.append(obstacle_velocity)
        
        # Compute the new velocity by taking into account the RVOs and the preferred velocity
        new_velocity = preferred_velocity
        for obstacle_velocity in obstacle_velocities:
            if (new_velocity - obstacle_velocity).dot(obstacle_velocity) > 0:
                new_velocity = obstacle_velocity
        
        return new_velocity

def normalize(vector):
    length = math.sqrt(vector.dot(vector))
    if length > 0:
        return vector / length
    else:
        return vector

# Simulation parameters
max_speed = 2.0
time_horizon = 5.0
time_step = 0.1

# Initialize agents
agent1 = Agent([0, 0], [0, 0], [5, 5])
agent2 = Agent([5, 0], [0, 0], [0, 5])
agents = [agent1, agent2]

# Simulate agent movements
for i in range(50):
    for agent in agents:
        new_velocity = agent.compute_new_velocity(agents)
        agent.velocity = normalize(new_velocity) * max_speed
        agent.position += agent.velocity * time_step



# ORCA

import math

class Agent:
    def __init__(self, position, velocity, radius, goal):
        self.position = position
        self.velocity = velocity
        self.radius = radius
        self.goal = goal
    
    def compute_new_velocity(self, agents, time_step):
        # Compute the ORCA constraints for all other agents
        orca_lines = []
        for agent in agents:
            if agent != self:
                relative_position = agent.position - self.position
                relative_velocity = self.velocity - agent.velocity
                distance = math.sqrt(relative_position.dot(relative_position))
                time_to_collision = (relative_position.dot(relative_velocity) + math.sqrt((relative_position.dot(relative_velocity))**2 - relative_velocity.dot(relative_velocity)*(distance**2 - self.radius**2))) / relative_velocity.dot(relative_velocity)
                if time_to_collision > 0 and time_to_collision < time_horizon:
                    if relative_position.dot(relative_velocity) < 0:
                        # Agent is moving towards us, need to avoid collision
                        projection = relative_position - relative_velocity * time_to_collision
                        orca_lines.append((normalize(projection), -projection.dot(self.position - agent.position)))
                    else:
                        # Agent is moving away from us, don't need to avoid collision
                        pass
        
        # Compute the new velocity by solving the linear program
        new_velocity = self.velocity
        num_orca_lines = len(orca_lines)
        if num_orca_lines > 0:
            A = [[0.0, 0.0] for i in range(num_orca_lines)]
            b = [0.0] * num_orca_lines
            invTimeStep = 1.0 / time_step
            for i, (line, offset) in enumerate(orca_lines):
                A[i][0] = line[1]
                A[i][1] = -line[0]
                b[i] = offset - line[0] * self.position[0] - line[1] * self.position[1]
            x = solve_linear_program(A, b, new_velocity, self.radius, invTimeStep)
            new_velocity = x
    
        # Apply velocity scaling and limit the speed
        new_velocity = normalize(new_velocity) * max_speed
        if new_velocity.dot(self.goal - self.position) > 0:
            # If the new velocity moves us closer to the goal, use it
            self.velocity = new_velocity
        else:
            # Otherwise, keep moving towards the goal
            self.velocity = normalize(self.goal - self.position) * max_speed
        
        self.position += self.velocity * time_step

    def normalize(vector):
        length = math.sqrt(vector.dot(vector))
        if length > 0:
            return vector / length
        else:
            return vector

    def solve_linear_program(lines, offsets, current_velocity, max_speed, invTimeStep):
        num_lines = len(lines)
        c = [0.0] * 2 * num_lines
        for i in range(num_lines):
            c[2*i] = lines[i][1]
            c[2*i+1] = -lines[i][0]
        vLine = [0.0] * 2
        x = [0.0] * 2
        solver = LinearProgrammingSolver(num_lines, 2)
        for i in range(num_lines):
            vLine[0] = lines[i][0]
            vLine[1] = lines[i][1]
            solver.setLine(i, vLine, offsets[i])
            x = [0.0] * dim
        best_solution = current_velocity
        best_distance = float("inf")
        for i in range(num_lines):
            line_i = self.lines[i]
            offset_i = self.offsets[i]
            for j in range(i + 1, num_lines):
                line_j = self.lines[j]
                offset_j = self.offsets[j]
                det = line_i[0] * line_j[1] - line_i[1] * line_j[0]
                if abs(det) < eps:
                    continue
                intersection = [(line_i[1] * offset_j - line_j[1] * offset_i) / det,
                                (line_j[0] * offset_i - line_i[0] * offset_j) / det]
                if line_i.dot(intersection - self.velocity) < 0 or line_j.dot(intersection - self.velocity) < 0:
                    continue
                distance = (intersection - current_velocity).dot(intersection - current_velocity)
                if distance < best_distance:
                    x = intersection
                    best_solution = intersection - current_velocity
                    best_distance = distance

        # Check if the new velocity violates any of the constraints
        for i in range(num_lines):
            if self.lines[i].dot(best_solution) + self.offsets[i] < 0:
                line = self.lines[i]
                proj = best_solution.dot(line) / line.dot(line)
                best_solution -= proj * line

        return best_solution

   
