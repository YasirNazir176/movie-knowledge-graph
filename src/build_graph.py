
import pandas as pd

from pathlib import Path
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import RDF, XSD
from urllib.parse import quote


# ==================================
# 1. PROJECT PATHS
# ==================================

BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)


# ==================================
# 2. LOAD CSV FILES
# ==================================

movies = pd.read_csv(DATA_DIR / "movies.csv")

ratings = pd.read_csv(DATA_DIR / "ratings.csv")

tags = pd.read_csv(DATA_DIR / "tags.csv")

links = pd.read_csv(
    DATA_DIR / "links.csv",
    dtype={"imdbId": "string", "tmdbId": "string"}
)

print("All CSV files loaded successfully!")


# ==================================
# 3. CREATE RDF GRAPH
# ==================================

g = Graph()

EX = Namespace("http://example.org/movie-ontology#")

g.bind("ex", EX)

# Load ontology definitions into the graph
ontology_file = OUTPUT_DIR / "movie_ontology.owl"

g.parse(str(ontology_file), format="xml")

print("Ontology loaded successfully!")


# ==================================
# 4. HELPER FUNCTIONS
# ==================================

def movie_uri(movie_id):
    return EX[f"Movie/{int(movie_id)}"]


def user_uri(user_id):
    return EX[f"User/{int(user_id)}"]


def genre_uri(genre):
    return EX[f"Genre/{quote(str(genre), safe='')}"]


def tag_uri(index):
    return EX[f"Tag/{index}"]


def rating_uri(index):
    return EX[f"Rating/{index}"]


# ==================================
# 5. CREATE MOVIE NODES
# ==================================

for _, row in movies.iterrows():

    movie = movie_uri(row["movieId"])

    g.add((movie, RDF.type, EX.Movie))

    g.add((
        movie,
        EX.movieId,
        Literal(int(row["movieId"]), datatype=XSD.integer)
    ))

    g.add((
        movie,
        EX.movieTitle,
        Literal(str(row["title"]), datatype=XSD.string)
    ))

    # Create Genre nodes and relationships
    for genre in str(row["genres"]).split("|"):

        if genre == "(no genres listed)":
            continue

        genre_node = genre_uri(genre)

        g.add((genre_node, RDF.type, EX.Genre))

        g.add((
            genre_node,
            EX.genreName,
            Literal(genre, datatype=XSD.string)
        ))

        g.add((movie, EX.hasGenre, genre_node))


print("Movie and Genre nodes created!")


# ==================================
# 6. CREATE USER AND RATING NODES
# ==================================

for index, row in ratings.iterrows():

    user = user_uri(row["userId"])
    movie = movie_uri(row["movieId"])

    rating = rating_uri(index)

    # User node
    g.add((user, RDF.type, EX.User))

    g.add((
        user,
        EX.userId,
        Literal(int(row["userId"]), datatype=XSD.integer)
    ))

    # Rating node
    g.add((rating, RDF.type, EX.Rating))

    g.add((
        rating,
        EX.ratingValue,
        Literal(float(row["rating"]), datatype=XSD.float)
    ))

    g.add((
        rating,
        EX.timestamp,
        Literal(int(row["timestamp"]), datatype=XSD.integer)
    ))

    # Relationships
    g.add((user, EX.rated, movie))

    g.add((rating, EX.ratedBy, user))

    g.add((rating, EX.ratingForMovie, movie))


print("User and Rating nodes created!")


# ==================================
# 7. CREATE TAG NODES
# ==================================

for index, row in tags.iterrows():

    user = user_uri(row["userId"])
    movie = movie_uri(row["movieId"])

    tag = tag_uri(index)

    # User node
    g.add((user, RDF.type, EX.User))

    g.add((
        user,
        EX.userId,
        Literal(int(row["userId"]), datatype=XSD.integer)
    ))

    # Tag node
    g.add((tag, RDF.type, EX.Tag))

    g.add((
        tag,
        EX.tagName,
        Literal(str(row["tag"]), datatype=XSD.string)
    ))

    g.add((
        tag,
        EX.tagTimestamp,
        Literal(int(row["timestamp"]), datatype=XSD.integer)
    ))

    # Relationships
    g.add((user, EX.addedTag, tag))

    g.add((movie, EX.hasTag, tag))

    g.add((tag, EX.taggedBy, user))

    g.add((tag, EX.tagForMovie, movie))


print("Tag nodes created!")


# ==================================
# 8. ADD IMDb AND TMDb LINKS
# ==================================

for _, row in links.iterrows():

    movie = movie_uri(row["movieId"])

    if pd.notna(row["imdbId"]):

        g.add((
            movie,
            EX.imdbId,
            Literal(str(row["imdbId"]), datatype=XSD.string)
        ))

    if pd.notna(row["tmdbId"]):

        g.add((
            movie,
            EX.tmdbId,
            Literal(str(row["tmdbId"]), datatype=XSD.string)
        ))


print("IMDb and TMDb IDs added!")


# ==================================
# 9. SAVE KNOWLEDGE GRAPH
# ==================================

output_file = OUTPUT_DIR / "movie_knowledge_graph.ttl"

g.serialize(
    destination=str(output_file),
    format="turtle"
)


# ==================================
# 10. DISPLAY RESULTS
# ==================================

print("\n=================================")
print("MOVIE KNOWLEDGE GRAPH CREATED!")
print("=================================")

print("Total RDF triples:", len(g))

print("Movies:", len(movies))
print("Ratings:", len(ratings))
print("Tags:", len(tags))
print("Users:", ratings["userId"].nunique())

print("\nSaved at:", output_file)
