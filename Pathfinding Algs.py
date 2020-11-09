import pygame
from win32api import GetSystemMetrics
import random
import time
pygame.init()
class Graph:
    def __init__(self):
        self.graph_dict = {}
    def add_vertex(self, vertex):
        self.graph_dict[vertex] = set()
    def add_edge(self, start_vertex, end_vertex):
        self.graph_dict[start_vertex].add(end_vertex)
        self.graph_dict[end_vertex].add(start_vertex)

visited = []
def bfs(graph, start, end):
    global visited
    path = [start]
    vertex_and_path = [start, path]
    bfs_queue = [vertex_and_path]
    while bfs_queue:
        current, path = bfs_queue.pop(0)
        visited.append(current)
        for neighbor in graph[current]:
            if neighbor not in visited:
                if neighbor == end:
                    return path + [neighbor]
                else:
                    bfs_queue.append([neighbor, path + [neighbor]])

amt_nodes = int(input("How Many Nodes Should Be In This Graph? (Min: 10, Max: 10000): "))
if amt_nodes < 10:
    raise Exception("BORING! Go Higher!")
elif amt_nodes > 10000:
    raise Exception("Are You Trying To Crash Your Computer?")

def random_num_gen(upper_bound = amt_nodes):
    return random.randint(1, upper_bound)

graph = Graph()
vertices = []
def create_graph():
    global vertices
    i = 1
    while i <= amt_nodes:
        graph.add_vertex(i)
        i += 1
    vertices = list(graph.graph_dict.keys())
    for vertex in vertices:
        random_number = random_num_gen()
        if random_number == vertex:
            random_number = random_num_gen()
        graph.add_edge(vertex, random_number)

create_graph()
size = width, height = GetSystemMetrics(0) - 20, GetSystemMetrics(1) - 20
screen = pygame.display.set_mode(size)
gray = 30, 30, 30
red = 230, 0, 0
yellow = 230, 230, 0
green = 0, 230, 0
blue = 0, 0, 230
aqua = 0, 60, 115
purple = 115, 0, 115
white = 200, 200, 200

pos_dict = {}
for node in vertices:
    pos_dict[node] = (random_num_gen(width), random_num_gen(height))
positions = pos_dict.keys()
start_node = random_num_gen()
end_node = random_num_gen()
path = bfs(graph.graph_dict, start_node, end_node)
screen.fill(gray)
for position in positions:
    for neighbor in graph.graph_dict[position]:
        pygame.draw.line(screen, white, pos_dict[position], pos_dict[neighbor], 1)
    if position == start_node:
        pygame.draw.circle(screen, blue, pos_dict[position], 5)
    elif position == end_node:
        pygame.draw.circle(screen, green, pos_dict[position], 5)
    else:
        pygame.draw.circle(screen, red, pos_dict[position], 5)
pygame.display.update()
if path:
    time.sleep(5)
    pygame.draw.circle(screen, blue, pos_dict[start_node], 6)
    pygame.draw.circle(screen, green, pos_dict[end_node], 6)
    pygame.event.pump()
    for vertex in visited:
        if vertex == start_node:
            pass
        elif vertex in path:
            pygame.draw.circle(screen, yellow, pos_dict[vertex], 6)
        elif vertex in visited:
            pygame.draw.circle(screen, purple, pos_dict[vertex], 6)
        pygame.display.update()
        pygame.event.pump()
        time.sleep(0.5)
    i = 0
    for vertex in path:
        time.sleep(0.5)
        try:
            pygame.draw.line(screen, aqua, pos_dict[vertex], pos_dict[path[i + 1]], 3)
            i += 1
            pygame.display.update()
        except:
            pass
        finally:
            pygame.event.pump()
    while True:
        for event in pygame.event.get():
            if event == pygame.QUIT:
                quit()
else:
    print("Path Not Found")
    quit()