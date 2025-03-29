import os
import graphviz
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware 
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React default port
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


# Create static directory if it doesn't exist
os.makedirs("static", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

class FolderRequest(BaseModel):
    folder_path: str
    output_filename: Optional[str] = "folder_structure"

def setup_graphviz():
    """Configure Graphviz path (Windows fix)"""
    try:
        os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'
    except Exception as e:
        print(f"Warning: Could not update PATH. Graphviz might not work. Error: {e}")

def validate_folder_path(folder_path: str):
    """Validate the folder path exists and is accessible"""
    if not os.path.exists(folder_path):
        raise HTTPException(
            status_code=400,
            detail=f"Path does not exist: {folder_path}"
        )
    if not os.path.isdir(folder_path):
        raise HTTPException(
            status_code=400,
            detail=f"Path is not a directory: {folder_path}"
        )
    try:
        os.listdir(folder_path)  # Test directory accessibility
    except PermissionError:
        raise HTTPException(
            status_code=403,
            detail=f"Permission denied for directory: {folder_path}"
        )

def generate_structure(folder_path: str, output_filename: str):
    """Generate the folder structure graph and text representation"""
    setup_graphviz()
    
    dot = graphviz.Digraph(
        comment="Folder Structure",
        format="png",
        engine="dot",
        graph_attr={"rankdir": "TB", "nodesep": "0.4"},
        node_attr={"shape": "box", "fontname": "Arial"},
        edge_attr={"color": "#666666"}
    )

    tree_structure = []
    node_counter = 0

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
            
            node_id = f"node_{node_counter}"
            node_counter += 1
            
            dot.node(node_id, item)
            dot.edge(parent_name, node_id)
            
            prefix = "    " * indent
            connector = "└── " if is_last else "├── "
            tree_structure.append(f"{prefix}{connector}{item}")
            
            if os.path.isdir(item_path):
                add_nodes_and_edges(node_id, item_path, indent + 1)

    root_name = "root"
    root_label = os.path.basename(os.path.normpath(folder_path))
    dot.node(root_name, root_label)
    tree_structure.append(f"{root_label}")

    add_nodes_and_edges(root_name, folder_path)

    try:
        # Save graph image
        output_path = dot.render(
            filename=output_filename,
            directory="static",
            cleanup=True,
            view=False
        )
        
        # Save text tree
        tree_str = "\n".join(tree_structure)
        txt_path = f"static/{output_filename}.txt"
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(tree_str)

        return {
            "image_path": f"/static/{output_filename}.png",
            "text_path": f"/static/{output_filename}.txt",
            "tree_structure": tree_str
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error during rendering: {str(e)}"
        )

@app.post("/generate-folder-structure")
async def generate_folder_structure(request: FolderRequest):
    """Endpoint to generate folder structure graph and text representation"""
    try:
        validate_folder_path(request.folder_path)
        result = generate_structure(request.folder_path, request.output_filename)
        return JSONResponse({
            "status": "success",
            "message": "Folder structure generated successfully",
            "data": {
                "image_url": result["image_path"],
                "text_url": result["text_path"],
                "tree_structure": result["tree_structure"]
            }
        })
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )

@app.get("/get-image/{filename}")
async def get_image(filename: str):
    """Endpoint to retrieve the generated image"""
    file_path = f"static/{filename}"
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="Image file not found. Generate it first using /generate-folder-structure"
        )
    return FileResponse(file_path)

@app.get("/get-text/{filename}")
async def get_text(filename: str):
    """Endpoint to retrieve the generated text file"""
    file_path = f"static/{filename}.txt"  # Note the .txt extension
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="Text file not found. Generate it first using /generate-folder-structure"
        )
    return FileResponse(file_path, media_type="text/plain")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)