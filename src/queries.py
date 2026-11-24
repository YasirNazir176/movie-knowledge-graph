
from rdflib import Graph, Namespace

# Load Knowledge Graph
kg = Graph()

kg.parse(
    "output/movie_knowledge_graph.ttl",
    format="turtle"
)

EX = Namespace("http://example.org/movie-ontology#")

print("Movie Knowledge Graph Loaded!")
print("=" * 50)


def run_query(title, query):
    print(f"\n{title}")
    print("-" * 50)

    results = kg.query(query)

    for row in results:
        print(" | ".join(str(value) for value in row))


# Query 1: Display first 10 movies
query1 = """
SELECT ?movie ?title
WHERE {
    ?movie a <http://example.org/movie-ontology#Movie> .
    ?movie <http://example.org/movie-ontology#movieTitle> ?title .
}
LIMIT 10
"""

run_query("1. First 10 Movies", query1)


# Query 2: Find all genres
query2 = """
SELECT DISTINCT ?genreName
WHERE {
    ?genre a <http://example.org/movie-ontology#Genre> .
    ?genre <http://example.org/movie-ontology#genreName> ?genreName .
}
ORDER BY ?genreName
LIMIT 20
"""

run_query("2. Movie Genres", query2)


# Query 3: Find ratings of Toy Story
query3 = """
SELECT ?userId ?ratingValue
WHERE {
    ?user <http://example.org/movie-ontology#rated> <http://example.org/movie-ontology#Movie/1> .
    ?user <http://example.org/movie-ontology#userId> ?userId .

    ?rating <http://example.org/movie-ontology#ratedBy> ?user .
    ?rating <http://example.org/movie-ontology#ratingForMovie> <http://example.org/movie-ontology#Movie/1> .
    ?rating <http://example.org/movie-ontology#ratingValue> ?ratingValue .
}
LIMIT 10
"""

run_query("3. Toy Story Ratings", query3)


# Query 4: Find movies with their genres
query4 = """
SELECT ?title ?genreName
WHERE {
    ?movie <http://example.org/movie-ontology#movieTitle> ?title .
    ?movie <http://example.org/movie-ontology#hasGenre> ?genre .
    ?genre <http://example.org/movie-ontology#genreName> ?genreName .
}
LIMIT 15
"""

run_query("4. Movies and Genres", query4)


print("\nSPARQL Queries Completed!")
