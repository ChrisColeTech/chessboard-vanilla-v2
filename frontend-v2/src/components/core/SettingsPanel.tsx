
interface SettingsPanelProps {
  onClose: () => void;
}

export function SettingsPanel({ onClose }: SettingsPanelProps) {
  return (
    <div className="card-gaming w-80 h-full p-6">
      <h2 className="text-xl font-bold mb-4">Settings</h2>
      <p className="text-muted-foreground mb-4">Settings panel placeholder</p>
      <button 
        onClick={onClose}
        className="px-4 py-2 bg-primary text-primary-foreground rounded"
      >
        Close
      </button>
    </div>
  );
}