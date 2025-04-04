import React, { useCallback } from 'react';
import { Box, Button, Typography } from '@mui/material';
import { CloudUpload } from '@mui/icons-material';

interface FileUploadProps {
  onFileSelect: (file: File) => void;
  accept?: string;
}

export const FileUpload: React.FC<FileUploadProps> = ({
  onFileSelect,
  accept = '.xlsx,.xls',
}) => {
  const handleFileChange = useCallback(
    (event: React.ChangeEvent<HTMLInputElement>) => {
      const file = event.target.files?.[0];
      if (file) {
        onFileSelect(file);
      }
    },
    [onFileSelect]
  );

  return (
    <Box
      sx={{
        border: '2px dashed #ccc',
        borderRadius: 2,
        p: 3,
        textAlign: 'center',
        cursor: 'pointer',
        '&:hover': {
          borderColor: 'primary.main',
        },
      }}
    >
      <input
        type="file"
        accept={accept}
        onChange={handleFileChange}
        style={{ display: 'none' }}
        id="file-upload"
      />
      <label htmlFor="file-upload">
        <Button
          component="span"
          variant="contained"
          startIcon={<CloudUpload />}
          sx={{ mb: 2 }}
        >
          Seleziona File
        </Button>
        <Typography variant="body2" color="textSecondary">
          Trascina un file Excel o clicca per selezionarlo
        </Typography>
      </label>
    </Box>
  );
}; 