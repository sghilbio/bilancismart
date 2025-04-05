import React from 'react';

interface Column {
  field: string;
  headerName: string;
}

interface DataTableProps {
  data: any[];
  columns: Column[];
}

export const DataTable: React.FC<DataTableProps> = ({ data, columns }) => {
  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-background">
        <thead>
          <tr>
            {columns.map((column) => (
              <th
                key={column.field}
                className="px-6 py-3 text-left text-xs font-medium text-text-secondary uppercase tracking-wider"
              >
                {column.headerName}
              </th>
            ))}
          </tr>
        </thead>
        <tbody className="divide-y divide-background">
          {data.map((row, rowIndex) => (
            <tr key={rowIndex}>
              {columns.map((column) => (
                <td
                  key={column.field}
                  className="px-6 py-4 whitespace-nowrap text-sm text-text-primary"
                >
                  {row[column.field]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}; 