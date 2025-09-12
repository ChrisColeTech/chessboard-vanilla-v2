
interface InstructionsModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  instructions?: string[];
}

export function InstructionsModal({ isOpen, onClose, title, instructions }: InstructionsModalProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4">
      <div className="card-gaming max-w-md w-full p-6">
        <h2 className="text-xl font-bold mb-4">{title || "Instructions"}</h2>
        <div className="space-y-2 mb-6">
          {instructions?.map((instruction, index) => (
            <p key={index} className="text-muted-foreground">{instruction}</p>
          ))}
        </div>
        <button 
          onClick={onClose}
          className="px-4 py-2 bg-primary text-primary-foreground rounded"
        >
          Got it
        </button>
      </div>
    </div>
  );
}