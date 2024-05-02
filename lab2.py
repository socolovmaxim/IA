import pandas as pd
from collections import deque, defaultdict
import heapq

# Helper function to load the map from a CSV file
def load_map_from_csv(file_path):
    # Load the CSV file, ensuring the first column is used as the index
    df = pd.read_csv(file_path, index_col=0)
    # Convert all entries in the DataFrame to integers
    df = df.apply(pd.to_numeric)
    adj_list = {}
    cities = df.columns
    for city in cities:
        # Access the row corresponding to the city and create a list of tuples (neighbor, distance)
        connections = [(cities[i], df.iloc[i][city]) for i in range(len(cities)) if df.iloc[i][city] > 0]
        adj_list[city] = connections
    return adj_list

# Heuristic function for A* and Greedy
def heuristic(city, goal, heuristics):
    return heuristics[city]

# BFS
def breadth_first_search(graph, start, goal):
    queue = deque([[start]])
    visited = set()
    while queue:
        path = queue.popleft()
        node = path[-1]
        if node in visited:
            continue
        if node == goal:
            return path
        visited.add(node)
        for neighbor, _ in graph[node]:
            if neighbor not in visited:
                queue.append(path + [neighbor])
    return None

# DFS
def depth_first_search(graph, start, goal, path=None, visited=None):
    if visited is None:
        visited = set()
    if path is None:
        path = []
    path.append(start)
    visited.add(start)
    if start == goal:
        return path
    for neighbor, _ in graph[start]:
        if neighbor not in visited:
            result = depth_first_search(graph, neighbor, goal, path, visited)
            if result:
                return result
    path.pop()
    return None

# Uniform Cost Search
def uniform_cost_search(graph, start, goal):
    queue = [(0, [start])]  # (cost, path)
    visited = set()
    while queue:
        cost, path = heapq.heappop(queue)
        node = path[-1]
        if node in visited:
            continue
        if node == goal:
            return path
        visited.add(node)
        for neighbor, weight in graph[node]:
            if neighbor not in visited:
                heapq.heappush(queue, (cost + weight, path + [neighbor]))
    return None

# Greedy Best First Search
def greedy_best_first_search(graph, start, goal, heuristics):
    queue = [(heuristic(start, goal, heuristics), [start])]
    visited = set()
    while queue:
        _, path = heapq.heappop(queue)
        node = path[-1]
        if node in visited:
            continue
        if node == goal:
            return path
        visited.add(node)
        for neighbor, _ in graph[node]:
            if neighbor not in visited:
                heapq.heappush(queue, (heuristic(neighbor, goal, heuristics), path + [neighbor]))
    return None

# A-star Search
def a_star_search(graph, start, goal, heuristics):
    queue = [(0 + heuristic(start, goal, heuristics), 0, [start])]
    visited = set()
    while queue:
        est_total_cost, cost, path = heapq.heappop(queue)
        node = path[-1]
        if node in visited:
            continue
        if node == goal:
            return path
        visited.add(node)
        for neighbor, weight in graph[node]:
            if neighbor not in visited:
                heapq.heappush(queue, (cost + weight + heuristic(neighbor, goal, heuristics), cost + weight, path + [neighbor]))
    return None

# Bidirectional Search (simplified version)
def bidirectional_search(graph, start, goal):
    if start == goal:
        return [start]
    queue_start = deque([(start, [start])])
    queue_goal = deque([(goal, [goal])])
    visited_start = {start: [start]}
    visited_goal = {goal: [goal]}
    while queue_start and queue_goal:
        path = expand_bidirectional(graph, queue_start, visited_start, visited_goal)
        if path:
            return path
        path = expand_bidirectional(graph, queue_goal, visited_goal, visited_start, reverse=True)
        if path:
            return path
    return None

def expand_bidirectional(graph, queue, visited_from, visited_to, reverse=False):
    while queue:
        node, path = queue.popleft()
        for neighbor, _ in graph[node]:
            if neighbor in visited_to:
                if reverse:
                    return path[::-1] + visited_to[neighbor][1:]
                else:
                    return path + visited_to[neighbor][1:]
            elif neighbor not in visited_from:
                visited_from[neighbor] = path + [neighbor]
                queue.append((neighbor, path + [neighbor]))
    return None

# Main function to run the search algorithms
def main():
    file_path = 'map.csv'
    romania_map = load_map_from_csv(file_path)
    distance_to_bucharest = {"Arad":366, "Bucharest":0, "Craiova":160, "Drobita":242, "Eforie":161, "Fagaras":176, "Giurgiu":77, "Hirsova":151, "Iasi":226, "Lugoj":244, "Mehedia":241, "Neamt":234, "Oradea":380, "Pitesti":100, "RM":193, "Sibiu":253, "Timisoara":329, "Urziceni":80, "Vaslui":199, "Zerind":374}
    
    start_city = 'Sibiu'
    goal_city = 'Bucharest'
    
    print("Breadth-first Search Path:", breadth_first_search(romania_map, start_city, goal_city))
    print("Depth-first Search Path:", depth_first_search(romania_map, start_city, goal_city))
    print("Uniform Cost Search Path:", uniform_cost_search(romania_map, start_city, goal_city))
    print("Greedy Best First Search Path:", greedy_best_first_search(romania_map, start_city, goal_city, distance_to_bucharest))
    print("A-star Search Path:", a_star_search(romania_map, start_city, goal_city, distance_to_bucharest))
    print("Bidirectional Search Path:", bidirectional_search(romania_map, start_city, goal_city))

if __name__ == "__main__":
    main()
