import requests
import sys
from collections import deque

s = requests.Session()
URL = "https://api.github.com/user"


def get_following(username):
    response = s.request("GET", URL + username + "/following")
    json = response.json()
    return json["Following"]

def load_social_graph(graph, username):
    if not graph.get(username):
        following = get_following(username)
        graph[username] = following
        for usr in following:
            load_social_graph(graph, usr)

def algoritmo_bfs(graph, nodo_inicial, nodo_final):
    queue = deque([nodo_inicial])
    level = {nodo_inicial: 0}
    parent = {nodo_inicial: None}
    i = 1
    while queue:
        vertex = queue.popleft()
        for neighbor in graph[vertex]:
            if neighbor not in level:
                queue.append(neighbor)
                level[neighbor] = i
                parent[neighbor] = vertex
        i = i + 1
        if level.get(nodo_final):
            return level, parent
    return level, parent


def dinstancia_usuario(username_from, username_to):
    social_graph = dict()
    load_social_graph(social_graph, username_from)
    bfs_result = algoritmo_bfs(social_graph, username_from, username_to)
    print(
        "La distancia entre %s y %s es: %i"
        % (username_from, username_to, bfs_result[0][username_to])
    )

username_from = sys.argv[1]
username_to = sys.argv[2]
dinstancia_usuario(username_from, username_to)
