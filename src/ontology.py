
from pathlib import Path

from rdflib import Graph, Namespace, Literal
from rdflib.namespace import RDF, RDFS, OWL, XSD


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

# Create RDF graph
g = Graph()

# Define namespace
EX = Namespace("http://example.org/movie-ontology#")

g.bind("ex", EX)
g.bind("owl", OWL)
g.bind("rdfs", RDFS)
g.bind("xsd", XSD)


# ==================================
# 1. DEFINE ONTOLOGY
# ==================================

ontology = EX.MovieOntology

g.add((ontology, RDF.type, OWL.Ontology))
g.add((
    ontology,
    RDFS.label,
    Literal("Movie Knowledge Graph Ontology")
))


# ==================================
# 2. DEFINE CLASSES
# ==================================

classes = {
    EX.Movie: "Movie",
    EX.User: "User",
    EX.Genre: "Genre",
    EX.Tag: "Tag",
    EX.Rating: "Rating"
}

for class_uri, label in classes.items():

    g.add((class_uri, RDF.type, OWL.Class))
    g.add((class_uri, RDFS.label, Literal(label)))


# ==================================
# 3. OBJECT PROPERTIES
# ==================================

object_properties = {

    EX.rated: (EX.User, EX.Movie),

    EX.hasGenre: (EX.Movie, EX.Genre),

    EX.addedTag: (EX.User, EX.Tag),

    EX.hasTag: (EX.Movie, EX.Tag),

    EX.ratedBy: (EX.Rating, EX.User),

    EX.ratingForMovie: (EX.Rating, EX.Movie),

    EX.taggedBy: (EX.Tag, EX.User),

    EX.tagForMovie: (EX.Tag, EX.Movie)
}

for prop, (domain, range_) in object_properties.items():

    g.add((prop, RDF.type, OWL.ObjectProperty))
    g.add((prop, RDFS.domain, domain))
    g.add((prop, RDFS.range, range_))


# ==================================
# 4. DATA PROPERTIES
# ==================================

data_properties = {

    EX.movieId: (EX.Movie, XSD.integer),

    EX.movieTitle: (EX.Movie, XSD.string),

    EX.userId: (EX.User, XSD.integer),

    EX.genreName: (EX.Genre, XSD.string),

    EX.tagName: (EX.Tag, XSD.string),

    EX.ratingValue: (EX.Rating, XSD.float),

    EX.timestamp: (EX.Rating, XSD.integer),

    EX.tagTimestamp: (EX.Tag, XSD.integer),

    EX.imdbId: (EX.Movie, XSD.string),

    EX.tmdbId: (EX.Movie, XSD.string)
}

for prop, (domain, range_) in data_properties.items():

    g.add((prop, RDF.type, OWL.DatatypeProperty))
    g.add((prop, RDFS.domain, domain))
    g.add((prop, RDFS.range, range_))


# ==================================
# 5. SAVE ONTOLOGY
# ==================================

output_file = OUTPUT_DIR / "movie_ontology.owl"

g.serialize(
    destination=str(output_file),
    format="xml"
)

print("Movie Ontology created successfully!")
print("Total ontology triples:", len(g))
print("Saved at:", output_file)
