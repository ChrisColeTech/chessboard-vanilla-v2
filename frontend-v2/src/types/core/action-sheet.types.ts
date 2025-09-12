import type { LucideIcon } from 'lucide-react';

export interface ActionSheetAction {
  id: string;
  label: string;
  icon?: LucideIcon;
  variant?: 'default' | 'primary' | 'secondary' | 'destructive';
  onPress?: () => void;
}

export interface PageActions {
  id: string;
  actions: ActionSheetAction[];
}

export interface ActionSheetConfiguration {
  [pageId: string]: ActionSheetAction[];
}