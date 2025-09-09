import { type ComponentType } from "react";

export interface SegmentedControlOption {
  id: string;
  label: string;
  icon?: ComponentType<{ className?: string }>;
  description?: string;
}

interface SegmentedControlProps {
  options: SegmentedControlOption[];
  value: string;
  onChange: (value: string) => void;
  className?: string;
  size?: 'sm' | 'md' | 'lg';
  iconOnly?: boolean;
}

export function SegmentedControl({ 
  options, 
  value, 
  onChange, 
  className = '',
  size = 'md',
  iconOnly = false
}: SegmentedControlProps) {
  const sizeClasses = {
    sm: 'text-xs px-2 py-1.5',
    md: 'text-sm px-3 py-2', 
    lg: 'text-base px-4 py-3'
  };

  const iconSizeClasses = {
    sm: 'w-3 h-3',
    md: 'w-4 h-4',
    lg: 'w-5 h-5'
  };

  return (
    <div className={`inline-flex bg-muted rounded-lg p-1 border border-border ${className}`}>
      {options.map((option, index) => {
        const isActive = value === option.id;
        const Icon = option.icon;
        const isFirst = index === 0;
        const isLast = index === options.length - 1;

        return (
          <button
            key={option.id}
            onClick={() => onChange(option.id)}
            className={`
              relative flex items-center justify-center gap-1.5 transition-all duration-200 flex-1 min-w-0 font-medium
              ${sizeClasses[size]}
              ${isFirst ? 'rounded-l-md' : ''}
              ${isLast ? 'rounded-r-md' : ''}
              ${isActive 
                ? 'bg-background text-foreground shadow-md border border-border' 
                : 'text-muted-foreground hover:text-foreground hover:bg-background/50'
              }
            `}
            title={option.description}
          >
            {Icon && <Icon className={iconSizeClasses[size]} />}
            {!iconOnly && <span className="truncate whitespace-nowrap">{option.label}</span>}
          </button>
        );
      })}
    </div>
  );
}