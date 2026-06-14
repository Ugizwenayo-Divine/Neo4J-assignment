import plotly.graph_objects as go
from plotly.subplots import make_subplots
from neo4j import GraphDatabase

# Connect to Neo4j
driver = GraphDatabase.driver("neo4j://127.0.0.1:7687", auth=("neo4j", "Password@123"))

# ---- Fetch data from Neo4j ----
with driver.session() as session:
    # Task 1: Total intersections and roads
    result = session.run("""
        MATCH (n:Intersection)
        WITH count(n) AS total_intersections
        MATCH ()-[r:ROAD]->()
        RETURN total_intersections, count(r) AS total_roads
    """)
    record = result.single()
    total_intersections = record["total_intersections"]
    total_roads = record["total_roads"]
    print(f"Intersections: {total_intersections}, Roads: {total_roads}")

    # Task 6: Degree distribution
    result = session.run("""
		    MATCH (n:Intersection)
		    RETURN count(n) AS num_intersections, COUNT { (n)--() } AS degree;
    """)

    degrees = []
    degree_counts = []
    for record in result:
        degrees.append(record["degree"])
        degree_counts.append(record["num_intersections"])
    print("Degree distribution fetched!")

    # Task 7: Top 10 most connected intersections
    result = session.run("""
        MATCH (n:Intersection)
        WITH n, COUNT { (n)--() } AS degree
        RETURN n.id AS intersection_id, degree
        ORDER BY degree DESC
        LIMIT 10;
    """)
    top10_ids = []
    top10_degrees = []
    for record in result:
        top10_ids.append(str(record["intersection_id"]))
        top10_degrees.append(record["degree"])
    print("Top 10 fetched!")

    # Task 8: Intersection categories by degree
    result = session.run("""
        MATCH (n:Intersection)
        WITH n, COUNT { (n)--() } AS degree

        WITH n.id AS intersection, degree,
        CASE
            WHEN degree <= 2 THEN "Low"
            WHEN degree <= 4 THEN "Medium"
            ELSE "High"
        END AS category

        RETURN category, count(*) AS num_intersections
        ORDER BY num_intersections DESC;
    """)
    categories = []
    category_counts = []
    for record in result:
        categories.append(record["category"])
        category_counts.append(record["num_intersections"])
    print("Categories fetched!")

driver.close()

# ---- Build Dashboard ----
fig = make_subplots(
    rows=2,
    cols=2,
    subplot_titles=(
        "Network Overview",
        "Degree Distribution",
        "Top 10 Most Connected Intersections",
        "Intersection Categories by Degree",
    ),
    specs=[
        [{"type": "indicator"}, {"type": "xy"}],  # row 1: Indicator | Bar
        [{"type": "xy"}, {"type": "domain"}],  # row 2: Bar       | Pie
    ],
)

# 1. Network Overview (key metrics as text)
fig.add_trace(
    go.Indicator(
        mode="number",
        value=total_intersections,
        title={"text": "Total Intersections"},
    ),
    row=1,
    col=1,
)

# 2. Degree Distribution Bar Chart
fig.add_trace(go.Bar(x=degrees, y=degree_counts, marker_color="steelblue", name="Degree Distribution"), row=1, col=2)

# 3. Top 10 Most Connected Intersections
fig.add_trace(go.Bar(x=top10_ids, y=top10_degrees, marker_color="coral", name="Top 10 Intersections"), row=2, col=1)

# 4. Intersection Categories
fig.add_trace(go.Pie(labels=categories, values=category_counts, name="Categories"), row=2, col=2)

# Layout
fig.update_layout(title_text="US Road Network Dashboard", title_font_size=24, showlegend=False, height=700)

fig.show()
print("Dashboard opened in browser!")
