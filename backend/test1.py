import os
import graphviz

def generate_file_structure_graph(folder_path, output_filename="folder_structure"):
    # Ensure Graphviz is in PATH (Windows fix)
    try:
        os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'
    except Exception as e:
        print(f"Warning: Could not update PATH. Graphviz might not work. Error: {e}")

    # Initialize Graphviz diagram
    dot = graphviz.Digraph(
        comment="Folder Structure",
        format="png",
        engine="dot",
        graph_attr={"rankdir": "TB", "nodesep": "0.4"},
        node_attr={"shape": "box", "fontname": "Arial"},
        edge_attr={"color": "#666666"}
    )

    tree_structure = []
    node_counter = 0  # For unique node IDs

    def add_nodes_and_edges(parent_name, path, indent=0):
        nonlocal node_counter
        try:
            items = sorted(os.listdir(path))
        except PermissionError:
            error_node = f"perror_{node_counter}"
            dot.node(error_node, "Permission Denied", fillcolor="#ffdddd")
            dot.edge(parent_name, error_node)
            tree_structure.append("│   " * indent + "└── [Permission Denied]")
            node_counter += 1
            return

        for i, item in enumerate(items):
            is_last = i == len(items) - 1
            item_path = os.path.join(path, item)
            
            # Create unique node ID
            node_id = f"node_{node_counter}"
            node_counter += 1
            
            dot.node(node_id, item)
            dot.edge(parent_name, node_id)
            
            # Tree visualization
            prefix = "    " * indent
            connector = "└── " if is_last else "├── "
            tree_structure.append(f"{prefix}{connector}{item}")
            
            if os.path.isdir(item_path):
                add_nodes_and_edges(node_id, item_path, indent + 1)

    # Root node setup
    root_name = "root"
    root_label = os.path.basename(os.path.normpath(folder_path))
    dot.node(root_name, root_label)
    tree_structure.append(f"{root_label}")

    # Generate structure
    add_nodes_and_edges(root_name, folder_path)

    # Save outputs
    try:
        # Save graph image
        output_path = dot.render(
            filename=output_filename,
            cleanup=True,
            view=False
        )
        print(f"Graph saved as: {output_path}")

        # Save text tree
        tree_str = "\n".join(tree_structure)
        txt_path = f"{output_filename}.txt"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(tree_str)
        print(f"Text tree saved as: {txt_path}")

        # Print tree to console
        print("\nFolder Structure:")
        print(tree_str)

    except Exception as e:
        print(f"\nError during rendering: {str(e)}")
        if hasattr(dot, 'source'):
            print("\nGenerated DOT code:")
            print(dot.source)
        print("\nText structure:")
        print("\n".join(tree_structure))

# Example Usage
if __name__ == "__main__":
    folder_path = input("Enter the folder path: ").strip()
    if os.path.isdir(folder_path):
        generate_file_structure_graph(folder_path)
    else:
        print("Error: Invalid directory path")