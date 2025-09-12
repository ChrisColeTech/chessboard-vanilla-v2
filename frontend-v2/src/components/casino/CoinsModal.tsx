
interface CoinsModalProps {
  isOpen: boolean;
  onClose: () => void;
  coinBalance?: number;
}

export function CoinsModal({ isOpen, onClose, coinBalance }: CoinsModalProps) {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4">
      <div className="card-gaming max-w-md w-full p-6">
        <h2 className="text-xl font-bold mb-4">Coin Balance</h2>
        <p className="text-muted-foreground mb-6">
          Current balance: {coinBalance || 0} coins
        </p>
        <button 
          onClick={onClose}
          className="px-4 py-2 bg-primary text-primary-foreground rounded"
        >
          Close
        </button>
      </div>
    </div>
  );
}