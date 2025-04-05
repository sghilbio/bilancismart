import React, { useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { MdUpload } from 'react-icons/md';

interface FileUploadProps {
  onFileSelect: (file: File) => void;
}

export const FileUpload: React.FC<FileUploadProps> = ({ onFileSelect }) => {
  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      onFileSelect(acceptedFiles[0]);
    }
  }, [onFileSelect]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'application/vnd.ms-excel': ['.xls'],
      'text/csv': ['.csv']
    },
    multiple: false
  });

  return (
    <div
      {...getRootProps()}
      className={`border-2 border-dashed rounded-lg p-6 text-center cursor-pointer transition-colors ${
        isDragActive
          ? 'border-primary bg-primary/5'
          : 'border-background hover:border-primary/50'
      }`}
    >
      <input {...getInputProps()} />
      <MdUpload className="w-12 h-12 mx-auto mb-4 text-text-secondary" />
      {isDragActive ? (
        <p className="text-text-primary">Rilascia il file qui...</p>
      ) : (
        <div>
          <p className="text-text-primary mb-2">
            Trascina qui il file di bilancio o clicca per selezionarlo
          </p>
          <p className="text-sm text-text-secondary">
            Formati supportati: XLSX, XLS, CSV
          </p>
        </div>
      )}
    </div>
  );
}; 