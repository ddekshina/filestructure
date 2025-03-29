import os
import graphviz
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'
def generate_file_structure_graph(folder_path, output_filename="folder_structure"):
    # Create Digraph with explicit settings
    dot = graphviz.Digraph(
        comment="Folder Structure",
        format="png",
        engine="dot",
        graph_attr={"rankdir": "TB", "nodesep": "0.5"},
        node_attr={"shape": "box", "style": "filled", "fillcolor": "#E6E6FA"},
        edge_attr={"color": "#888888"}
    )
    
    # Create root node with simplified ID
    root_id = "root"
    dot.node(root_id, os.path.basename(folder_path))
    
    # Track nodes to avoid duplicates
    nodes = {folder_path: root_id}
    
    def add_nodes(parent_path, parent_id):
        try:
            for item in os.listdir(parent_path):
                item_path = os.path.join(parent_path, item)
                node_id = f"node_{len(nodes)}"
                
                dot.node(node_id, item)
                dot.edge(parent_id, node_id)
                nodes[item_path] = node_id
                
                if os.path.isdir(item_path):
                    add_nodes(item_path, node_id)
        except PermissionError:
            dot.node(f"error_{parent_id}", "Permission Denied", fillcolor="#FFCCCC")
            dot.edge(parent_id, f"error_{parent_id}")

    add_nodes(folder_path, root_id)
    
    # Explicit rendering with verification
    try:
        output_path = dot.render(
            filename=output_filename,
            format="png",
            cleanup=True,
            view=False
        )
        if os.path.exists(output_path):
            print(f"Success! Image saved to: {output_path}")
            return output_path
        else:
            print("Graphviz generated DOT but failed to create image")
            print("Generated DOT code:")
            print(dot.source)
            return None
    except Exception as e:
        print(f"Rendering failed: {str(e)}")
        return None

# Usage
folder_path = input("Enter folder path: ").strip()
if os.path.exists(folder_path):
    generate_file_structure_graph(folder_path)
else:
    print("Error: Path does not exist")