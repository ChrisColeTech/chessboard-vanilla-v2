import React, { useEffect } from 'react';
import { useHelpQueries } from '../../../hooks/help';

interface HelpComponentProps {
  className?: string;
}

export const HelpComponent: React.FC<HelpComponentProps> = ({
  className
}) => {
  const { data, loading, error, refetch } = useHelpQueries();
  
  // Load data on component mount
  useEffect(() => {
    refetch();
  }, []);
  
  const renderTable = () => {
    if (!data?.data || !Array.isArray(data.data)) {
      return <p>No data available</p>;
    }
    
    const items = data.data;
    if (items.length === 0) {
      return <p>No help records found</p>;
    }
    
    // Get column headers from the first item
    const columns = Object.keys(items[0]);
    
    return (
      <table style={{ width: '100%', borderCollapse: 'collapse', marginTop: '16px' }}>
        <thead>
          <tr>
            {columns.map((col: string) => (
              <th key={col} style={{ 
                border: '1px solid #ddd', 
                padding: '8px', 
                backgroundColor: '#f5f5f5',
                textAlign: 'left'
              }}>
                {col.charAt(0).toUpperCase() + col.slice(1).replace(/_/g, ' ')}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {items.map((item: any, index: number) => (
            <tr key={item.id || index}>
              {columns.map((col: string) => (
                <td key={col} style={{ 
                  border: '1px solid #ddd', 
                  padding: '8px'
                }}>
                  {typeof item[col] === 'object' ? JSON.stringify(item[col]) : String(item[col] ?? '')}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    );
  };
  
  return (
    <div className={`help-component ${className || ''}`} style={{ padding: '16px' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '16px' }}>
        <h2>Help Data</h2>
        <button 
          onClick={() => refetch()}
          disabled={loading}
          style={{
            padding: '8px 16px',
            backgroundColor: loading ? '#ccc' : '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: loading ? 'default' : 'pointer'
          }}
        >
          {loading ? 'Loading...' : 'Refresh'}
        </button>
      </div>
      
      {error && (
        <div style={{
          color: 'red', 
          backgroundColor: '#ffebee', 
          padding: '12px', 
          borderRadius: '4px', 
          marginBottom: '16px'
        }}>
          <strong>Error:</strong> {error}
        </div>
      )}
      
      {loading && !data && (
        <div style={{ textAlign: 'center', padding: '40px' }}>
          <p>Loading help data...</p>
        </div>
      )}
      
      {!loading && renderTable()}
    </div>
  );
};
