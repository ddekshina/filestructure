import React, { useState } from "react";
import { Button, TextField, Box, Typography, CircularProgress, Paper } from "@mui/material";
import { generateFolderStructure } from "../api/api";

export default function FolderVisualizer() {
  const [folderPath, setFolderPath] = useState("");
  const [outputFilename, setOutputFilename] = useState("folder_structure");
  const [isLoading, setIsLoading] = useState(false);
  const [imageUrl, setImageUrl] = useState(null); // Stores the image URL
  const [treeStructure, setTreeStructure] = useState(""); // Stores the text structure
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    setError(null);
    setImageUrl(null); // Reset image on new submission

    try {
      const response = await generateFolderStructure(folderPath, outputFilename);
      
      // Set the full image URL (assuming backend serves it at /static/)
      setImageUrl(`http://localhost:8000${response.data.image_url}`);
      
      // Set the tree structure text
      setTreeStructure(response.data.tree_structure);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to generate folder structure");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3 }}>
      <TextField
        label="Folder Path"
        value={folderPath}
        onChange={(e) => setFolderPath(e.target.value)}
        fullWidth
        required
        margin="normal"
      />
      <TextField
        label="Output Filename (optional)"
        value={outputFilename}
        onChange={(e) => setOutputFilename(e.target.value)}
        fullWidth
        margin="normal"
      />
      <Button
        type="submit"
        variant="contained"
        disabled={isLoading}
        sx={{ mt: 2 }}
      >
        {isLoading ? <CircularProgress size={24} /> : "Generate Structure"}
      </Button>

      {error && (
        <Typography color="error" sx={{ mt: 2 }}>
          Error: {error}
        </Typography>
      )}

      {/* Display the generated image */}
      {imageUrl && (
        <Box sx={{ mt: 4 }}>
          <Typography variant="h6" gutterBottom>
            Folder Structure Visualization
          </Typography>
          <Paper elevation={3} sx={{ p: 2, mb: 3 }}>
            <img 
              src={imageUrl} 
              alt="Generated folder structure" 
              style={{ maxWidth: "100%", height: "auto" }}
            />
          </Paper>
        </Box>
      )}

      {/* Display the tree structure as text */}
      {treeStructure && (
        <Box sx={{ mt: 2 }}>
          <Typography variant="h6" gutterBottom>
            Text Representation
          </Typography>
          <Paper elevation={3} sx={{ p: 2, fontFamily: "monospace", whiteSpace: "pre" }}>
            {treeStructure}
          </Paper>
        </Box>
      )}
    </Box>
  );
}