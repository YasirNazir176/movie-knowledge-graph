# Technical Rationale — Movie Knowledge Graph

**Course:** Knowledge Based Systems  
**Project:** Movie Knowledge Graph  
**Dataset:** MovieLens Latest Small

## 1. The Problem

Movie-related information is distributed across multiple CSV files. Movie titles and genres are stored in `movies.csv`, user ratings in `ratings.csv`, tags in `tags.csv`, and external movie identifiers in `links.csv`.

Although these files contain related information, their relationships are not explicitly represented as a connected knowledge structure.

For example, answering a question such as *"Which users rated Toy Story, what ratings did they give, and which genres does it belong to?"* requires combining information from multiple datasets.

The main challenge was to transform these separate records into a connected, meaningful, and machine-queryable Knowledge Graph.

## 2. Options Considered

We considered three approaches for implementing the project.

| Approach | Strength | Weakness for This Project |
|---|---|---|
| Traditional Relational Database (SQL) | Structured data storage and efficient table queries | Relationships require joins and do not directly provide RDF/OWL knowledge representation |
| **Python — RDFLib + SPARQL + NetworkX (Selected)** | Automated CSV-to-RDF conversion, ontology creation, semantic querying, and visualization | Requires Python programming and knowledge of graph modelling |
| Neo4j | Powerful graph database, Cypher queries, and interactive visualization | Requires additional database setup and a separate data import workflow |

## 3. Our Selection and Why

**Selected Approach: Python with RDFLib, SPARQL, NetworkX, and Matplotlib.**

We selected Python because the primary objective was to integrate existing movie datasets and represent their relationships as a Knowledge Graph rather than develop a web application or manage a production database.

Python provides a straightforward way to process multiple CSV files using Pandas and convert their records into RDF triples using RDFLib.

We designed an OWL ontology containing five main classes:

- **Movie:** Represents movies.
- **User:** Represents users who rate or tag movies.
- **Genre:** Represents movie genres.
- **Rating:** Represents individual user ratings.
- **Tag:** Represents user-generated tags.

We also defined object properties and datatype properties to describe relationships and store information about these entities.

### Generated Knowledge Graph Statistics

The successfully generated Knowledge Graph contains:

| Component | Total |
|---|---:|
| RDF Triples | 702,873 |
| Movies | 9,742 |
| Users | 610 |
| Ratings | 100,836 |
| Tag Records | 3,683 |
| Genres | 19 |

Relationships such as `hasGenre`, `rated`, `ratedBy`, `ratingForMovie`, `hasTag`, and `addedTag` connect the entities within the graph.

We selected SPARQL because it provides a standard way to retrieve information from RDF graphs. NetworkX and Matplotlib were used to generate a visual representation of the graph.

### Generated RDF and OWL Files

The project produces two important semantic web files:

- **`movie_ontology.owl`:** Contains the OWL ontology, including classes, object properties, and datatype properties.
- **`movie_knowledge_graph.ttl`:** Contains the complete RDF Knowledge Graph, including entities, relationships, and data.

The Turtle (`.ttl`) format provides a readable serialization of RDF data, while the OWL (`.owl`) file represents the ontology.

These files can be opened and explored using RDF-compatible tools such as Protégé.

## 4. Why Not the Other Approaches?

### Traditional SQL Database

A relational database can store the same information, but the main objective of this assignment is to demonstrate Knowledge Representation using RDF, OWL, and semantic relationships rather than only relational table operations.

### Neo4j

Neo4j is a powerful graph database with interactive visualization and Cypher query support. However, it introduces additional database configuration and import steps that were not necessary for this assignment.

### Why RDFLib?

RDFLib provides the functionality required for ontology loading, RDF graph construction, serialization, and SPARQL querying within a single Python-based workflow.

Therefore, it was the most suitable choice for the project's requirements.

## 5. Proof That It Works

We successfully executed four SPARQL validation queries against the generated Turtle Knowledge Graph.

| Query | Purpose |
|---|---|
| Movie Retrieval | Retrieves movie titles and their identifiers |
| Genre Retrieval | Retrieves all available movie genres |
| Movie Ratings | Retrieves users and their ratings for Toy Story |
| Movies and Genres | Retrieves movies and their associated genres |

All four queries executed successfully and returned results from the generated graph.

This demonstrates that the Knowledge Graph contains connected information that can be retrieved through semantic queries.

The project successfully generated:

- 702,873 RDF triples.
- An OWL ontology containing five main classes.
- A complete RDF Knowledge Graph in Turtle format.
- Four working SPARQL queries.
- A PNG visualization of a representative portion of the graph.

## 6. Risks and Limitations

### Dataset Limitations

The project uses the MovieLens Latest Small dataset. It is suitable for demonstrating Knowledge Graph construction but does not represent every movie, user, or rating in the real world.

### Visualization Limitations

The visualization displays a representative sample of the Knowledge Graph rather than all 702,873 RDF triples. Visualizing the complete graph would make the image crowded and difficult to interpret.

### Query Limitations

The implemented SPARQL queries demonstrate basic information retrieval and relationship traversal. More advanced capabilities, such as movie recommendations, rating-based ranking, and movie similarity analysis, have not been implemented.

## 7. Future Improvements

The project can be extended with the following features:

- Movie recommendation based on user ratings.
- Movie similarity analysis using genres and tags.
- Advanced SPARQL queries for discovering hidden relationships.
- Integration with a graph database such as Neo4j.
- An interactive interface for exploring the Knowledge Graph.
- Support for larger movie datasets.

## 8. Reproducibility and Fallback

The original MovieLens CSV files and generated RDF/OWL files are maintained separately.

This allows the Knowledge Graph to be rebuilt whenever the source dataset changes or the graph needs to be regenerated.

The project follows a modular workflow:

1. Validate the source CSV files.
2. Create the OWL ontology.
3. Build the RDF Knowledge Graph.
4. Execute SPARQL queries.
5. Generate graph visualization.

If the generated graph files are deleted or become corrupted, they can be recreated by running the project scripts in the correct order.

---

**Conclusion:** Python, RDFLib, OWL, and SPARQL provided a suitable approach for transforming separate MovieLens datasets into a connected and queryable Movie Knowledge Graph. The successful generation of 702,873 RDF triples and execution of four SPARQL queries demonstrate that the project meets its primary objectives.