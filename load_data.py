# In this file we split the data from usa.txt file into roads.csv and intersections.csv
# because those are the only supported extensions to import in NEO4J
import csv

INPUT_FILE = "usa.txt"

with open(INPUT_FILE, "r") as f:
    lines = [line.strip() for line in f if line.strip()]

# First line contains counts
num_nodes, num_edges = map(int, lines[0].split())

print(f"Nodes: {num_nodes}")
print(f"Edges: {num_edges}")

# Node section
node_lines = lines[1 : num_nodes + 1]

# Edge section
edge_lines = lines[num_nodes + 1 :]

print(f"Found node records: {len(node_lines)}")
print(f"Found edge records: {len(edge_lines)}")

# -----------------------
# intersections.csv
# -----------------------
with open("intersections.csv", "w", newline="") as f:
    writer = csv.writer(f)

    writer.writerow(["id", "x", "y"])

    for line in node_lines:
        node_id, x, y = line.split()
        writer.writerow([node_id, x, y])

# -----------------------
# roads.csv
# -----------------------
with open("roads.csv", "w", newline="") as f:
    writer = csv.writer(f)

    writer.writerow(["source", "target"])

    for line in edge_lines:
        source, target = line.split()
        writer.writerow([source, target])

print("CSV files created successfully!")
