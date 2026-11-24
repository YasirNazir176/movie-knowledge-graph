
from rdflib import Graph, Namespace, RDF, RDFS
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
TTL_FILE = BASE_DIR / "output" / "movie_knowledge_graph.ttl"
OUTPUT_FILE = BASE_DIR / "output" / "movie_knowledge_graph.png"

# Load knowledge graph
kg = Graph()
kg.parse(TTL_FILE, format="turtle")

EX = Namespace("http://example.org/movie-ontology#")

print("Knowledge Graph loaded successfully!")

# Select one movie for visualization
movie = EX["Movie/1"]

# Create a small NetworkX graph
G = nx.DiGraph()

def add_node(uri, label, node_type):
    G.add_node(uri, label=label, type=node_type)

def add_edge(source, target, relation):
    G.add_edge(source, target, label=relation)

# Get movie title
title = kg.value(movie, EX.movieTitle)

if title is None:
    title = "Movie 1"
else:
    title = str(title)

add_node(movie, title, "Movie")

# Add movie genres
for genre in kg.objects(movie, EX.hasGenre):
    genre_name = kg.value(genre, EX.genreName)
    genre_name = str(genre_name) if genre_name else "Genre"

    add_node(genre, genre_name, "Genre")
    add_edge(movie, genre, "hasGenre")

# Get users who rated this movie
users_added = 0

for user in kg.subjects(EX.rated, movie):

    if users_added >= 5:
        break

    user_id = kg.value(user, EX.userId)
    user_label = f"User {user_id}"

    add_node(user, user_label, "User")
    add_edge(user, movie, "rated")

    # Find rating records for this user and movie
    for rating in kg.subjects(EX.ratedBy, user):

        if (rating, EX.ratingForMovie, movie) in kg:
            rating_value = kg.value(rating, EX.ratingValue)

            rating_label = f"Rating: {rating_value}"

            add_node(rating, rating_label, "Rating")
            add_edge(user, rating, "gave")
            add_edge(rating, movie, "ratingForMovie")

            break

    users_added += 1

# Draw graph
plt.figure(figsize=(16, 10))

pos = nx.spring_layout(G, seed=42, k=1.5)

# Node colors by type
color_map = {
    "Movie": "orange",
    "User": "skyblue",
    "Genre": "lightgreen",
    "Rating": "pink"
}

node_colors = [
    color_map[G.nodes[node]["type"]]
    for node in G.nodes()
]

nx.draw_networkx_nodes(
    G, pos,
    node_color=node_colors,
    node_size=2200
)

nx.draw_networkx_labels(
    G, pos,
    labels=nx.get_node_attributes(G, "label"),
    font_size=8
)

nx.draw_networkx_edges(
    G, pos,
    arrows=True,
    arrowstyle="->",
    arrowsize=15
)

edge_labels = nx.get_edge_attributes(G, "label")

nx.draw_networkx_edge_labels(
    G, pos,
    edge_labels=edge_labels,
    font_size=7
)

plt.title("Movie Knowledge Graph - Sample Visualization")
plt.axis("off")
plt.tight_layout()

# Save image
plt.savefig(OUTPUT_FILE, dpi=300, bbox_inches="tight")
plt.show()

print("\nVisualization created successfully!")
print("Total sample nodes:", G.number_of_nodes())
print("Total sample edges:", G.number_of_edges())
print("Saved at:", OUTPUT_FILE)
