import React from 'react';
import { Container, CssBaseline, ThemeProvider, createTheme } from '@mui/material';
import FolderVisualizer from './components/FolderVisualizer';

const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <FolderVisualizer />
      </Container>
    </ThemeProvider>
  );
}

export default App;