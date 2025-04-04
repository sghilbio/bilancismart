import React from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  TablePagination,
} from '@mui/material';

interface DataTableProps {
  data: any[];
  columns: { field: string; headerName: string }[];
  title?: string;
}

export const DataTable: React.FC<DataTableProps> = ({
  data,
  columns,
  title,
}) => {
  const [page, setPage] = React.useState(0);
  const [rowsPerPage, setRowsPerPage] = React.useState(10);

  const handleChangePage = (event: unknown, newPage: number) => {
    setPage(newPage);
  };

  const handleChangeRowsPerPage = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    setRowsPerPage(parseInt(event.target.value, 10));
    setPage(0);
  };

  return (
    <Paper sx={{ width: '100%', mb: 2 }}>
      {title && (
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell colSpan={columns.length} align="center">
                  {title}
                </TableCell>
              </TableRow>
            </TableHead>
          </Table>
        </TableContainer>
      )}
      <TableContainer>
        <Table>
          <TableHead>
            <TableRow>
              {columns.map((column) => (
                <TableCell key={column.field}>{column.headerName}</TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {data
              .slice(page * rowsPerPage, page * rowsPerPage + rowsPerPage)
              .map((row, index) => (
                <TableRow key={index}>
                  {columns.map((column) => (
                    <TableCell key={column.field}>
                      {row[column.field]}
                    </TableCell>
                  ))}
                </TableRow>
              ))}
            {data.length === 0 && (
              <TableRow>
                <TableCell colSpan={columns.length} align="center">
                  Nessun dato disponibile
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>
      <TablePagination
        rowsPerPageOptions={[5, 10, 25]}
        component="div"
        count={data.length}
        rowsPerPage={rowsPerPage}
        page={page}
        onPageChange={handleChangePage}
        onRowsPerPageChange={handleChangeRowsPerPage}
        labelRowsPerPage="Righe per pagina:"
      />
    </Paper>
  );
}; 