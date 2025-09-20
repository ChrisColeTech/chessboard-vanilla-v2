import { useMemo } from 'react';
import type { DataTableColumn } from '../../types/ui/data-table.types';

export const useDataTableColumns = (data: any[]): DataTableColumn[] => {
  return useMemo(() => {
    if (!data || data.length === 0) return [];
    
    const firstItem = data[0];
    return Object.keys(firstItem).map(key => ({
      key,
      header: key.charAt(0).toUpperCase() + key.slice(1).replace(/([A-Z])/g, ' $1').trim(),
      render: (value: any) => {
        if (value === null || value === undefined) return '-';
        if (typeof value === 'boolean') return value ? 'Yes' : 'No';
        if (typeof value === 'object') return JSON.stringify(value);
        return String(value);
      }
    }));
  }, [data]);
};

export default useDataTableColumns;