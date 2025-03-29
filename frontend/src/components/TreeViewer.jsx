import React from 'react';
import { Paper, Typography } from '@mui/material';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { atomDark } from 'react-syntax-highlighter/dist/esm/styles/prism';

const TreeViewer = ({ content }) => {
  return (
    <Paper elevation={0} sx={{ p: 2, bgcolor: 'background.default' }}>
      <Typography variant="h6" gutterBottom>
        Folder Structure Tree
      </Typography>
      <SyntaxHighlighter
        language="text"
        style={atomDark}
        showLineNumbers
        wrapLines
        customStyle={{ margin: 0, borderRadius: 4 }}
      >
        {content}
      </SyntaxHighlighter>
    </Paper>
  );
};

export default TreeViewer;