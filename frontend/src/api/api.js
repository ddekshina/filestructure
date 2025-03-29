import axios from "axios";

const API_BASE_URL = "http://localhost:8000"; // FastAPI default port

export const generateFolderStructure = async (folderPath, outputFilename) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/generate-folder-structure`, {
      folder_path: folderPath,
      output_filename: outputFilename,
    });
    return response.data;
  } catch (error) {
    console.error("Error generating folder structure:", error);
    throw error;
  }
};

export const getImage = async (filename) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/get-image/${filename}`, {
      responseType: "blob", // Important for file downloads
    });
    return response.data;
  } catch (error) {
    console.error("Error fetching image:", error);
    throw error;
  }
};

export const getTextFile = async (filename) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/get-text/${filename}`);
    return response.data;
  } catch (error) {
    console.error("Error fetching text file:", error);
    throw error;
  }
};