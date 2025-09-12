import { Settings } from "lucide-react";
import { Button } from "../ui/button";

interface HeaderProps {
  onOpenSettings: () => void;
  coinBalance?: number;
}

export function Header({ onOpenSettings, coinBalance }: HeaderProps) {
  return (
    <div className="glass-layout px-4 py-2 flex items-center justify-between">
      <div className="flex-1" />
      
      <div className="flex items-center gap-2">
        {coinBalance !== undefined && (
          <div className="text-sm font-medium text-muted-foreground">
            Balance: {coinBalance}
          </div>
        )}
        
        <Button
          variant="ghost"
          size="sm"
          onClick={onOpenSettings}
          className="h-8 w-8 p-0"
        >
          <Settings className="h-4 w-4" />
        </Button>
      </div>
    </div>
  );
}
