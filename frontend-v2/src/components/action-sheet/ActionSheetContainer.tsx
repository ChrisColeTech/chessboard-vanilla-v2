
interface ActionSheetContainerProps {
  onClose: () => void;
  isOpen: boolean;
  onOpenSettings: () => void;
}

export function ActionSheetContainer({ onClose, isOpen, onOpenSettings }: ActionSheetContainerProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-40 bg-black/50 flex items-end justify-center p-4">
      <div className="card-gaming w-full max-w-md p-6">
        <h2 className="text-xl font-bold mb-4">Menu</h2>
        <div className="space-y-2">
          <button 
            onClick={onOpenSettings}
            className="w-full text-left px-4 py-2 hover:bg-accent rounded"
          >
            Settings
          </button>
          <button 
            onClick={onClose}
            className="w-full text-left px-4 py-2 hover:bg-accent rounded"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}