import React, { useEffect, useState } from 'react';
import { DYNAMIC_PAGE_ACTIONS } from '../../constants/actions/page-actions.dynamic';
import { useActionSheet } from '../../contexts/ActionSheetContext';
import type { ActionSheetAction } from '../../types/core/action-sheet.types';

export const ActionSheetContainer: React.FC = () => {
  const { isOpen, currentPage, closeActionSheet } = useActionSheet();
  const [delayedActionSheetPage, setDelayedActionSheetPage] = useState<string | null>(null);

  // Delay loading to ensure dynamic system is initialized
  useEffect(() => {
    if (currentPage) {
      const timer = setTimeout(() => {
        setDelayedActionSheetPage(currentPage);
      }, 100);
      return () => clearTimeout(timer);
    } else {
      setDelayedActionSheetPage(null);
    }
  }, [currentPage]);

  if (!isOpen || !delayedActionSheetPage) {
    return null;
  }

  // Get actions from dynamic system
  const actions = DYNAMIC_PAGE_ACTIONS[delayedActionSheetPage] || [];

  return (
    <div className="fixed inset-0 z-50 flex items-end justify-center p-4 pointer-events-auto">
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-black bg-opacity-50"
        onClick={closeActionSheet}
      />
      
      {/* Action Sheet */}
      <div className="relative bg-white rounded-lg shadow-xl max-w-md w-full max-h-96 overflow-y-auto">
        <div className="p-4">
          <h3 className="text-lg font-semibold mb-4">
            Actions for {delayedActionSheetPage}
          </h3>
          
          {actions.length === 0 ? (
            <p className="text-gray-500 text-center py-8">
              No actions available for this page
            </p>
          ) : (
            <div className="space-y-2">
              {actions.map((action: ActionSheetAction) => (
                <button
                  key={action.id}
                  className={`w-full flex items-center justify-between p-3 rounded-lg transition-colors ${
                    action.variant === 'primary' 
                      ? 'bg-blue-600 hover:bg-blue-700 text-white'
                      : action.variant === 'destructive'
                      ? 'bg-red-600 hover:bg-red-700 text-white'
                      : 'bg-gray-100 hover:bg-gray-200 text-gray-900'
                  }`}
                  onClick={() => {
                    action.onPress?.();
                    console.log(`Action pressed: ${action.id}`);
                  }}
                >
                  <span className="flex items-center">
                    {action.icon && <action.icon className="w-5 h-5 mr-3" />}
                    {action.label}
                  </span>
                </button>
              ))}
            </div>
          )}
          
          <button
            onClick={closeActionSheet}
            className="w-full mt-4 p-3 bg-gray-200 hover:bg-gray-300 text-gray-900 rounded-lg transition-colors"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
};