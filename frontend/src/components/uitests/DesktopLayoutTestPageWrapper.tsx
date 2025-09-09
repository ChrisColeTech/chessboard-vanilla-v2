import React from 'react';
import { usePageInstructions } from '../../hooks/core/usePageInstructions';
import { DesktopLayoutTestPage } from '../../pages/uitests/DesktopLayoutTestPage';

export const DesktopLayoutTestPageWrapper: React.FC = () => {
  usePageInstructions('desktoplayouttest');
  
  return <DesktopLayoutTestPage />;
};