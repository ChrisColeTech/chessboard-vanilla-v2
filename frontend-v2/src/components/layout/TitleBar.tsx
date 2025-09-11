import { Coins } from "lucide-react";

interface TitleBarProps {
  coinBalance: number;
}

export function TitleBar({ coinBalance }: TitleBarProps) {
  return (
    <div className="flex items-center justify-between w-full px-4 py-3 bg-card border-b border-border">
      <div className="flex items-center space-x-3">
        <h1 className="text-xl font-bold text-foreground">Chess App</h1>
      </div>
      
      <div className="flex items-center space-x-2 text-sm text-muted-foreground">
        <Coins className="w-4 h-4" />
        <span className="font-medium">{coinBalance.toLocaleString()}</span>
      </div>
    </div>
  );
}
