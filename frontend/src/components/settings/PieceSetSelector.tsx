import { Crown, Shield, Swords, Briefcase, Zap } from "lucide-react";
import { SegmentedControl, type SegmentedControlOption } from "../ui/SegmentedControl";
import { useAppStore } from "../../stores/appStore";
import { PIECE_SETS, PIECE_SET_NAMES } from "../../constants/pieces.constants";

// Icons for each piece set
const PIECE_SET_ICONS = {
  classic: Crown,
  modern: Shield, 
  tournament: Swords,
  executive: Briefcase,
  conqueror: Zap
} as const;

export function PieceSetSelector() {
  const selectedPieceSet = useAppStore((state) => state.selectedPieceSet);
  const setPieceSet = useAppStore((state) => state.setPieceSet);

  const pieceSetOptions: SegmentedControlOption[] = Object.entries(PIECE_SETS).map(([key]) => ({
    id: key,
    label: PIECE_SET_NAMES[key as keyof typeof PIECE_SET_NAMES],
    icon: PIECE_SET_ICONS[key as keyof typeof PIECE_SET_ICONS],
    description: `${PIECE_SET_NAMES[key as keyof typeof PIECE_SET_NAMES]} piece set`
  }));

  const SelectedIcon = PIECE_SET_ICONS[selectedPieceSet];

  return (
    <div>
      <div className="flex items-center gap-2 mb-3">
        <h3 className="text-base font-semibold text-foreground flex items-center gap-2">
          <Crown className="w-4 h-4" />
          Piece Set
        </h3>
        <div className="flex items-center gap-1 text-xs text-muted-foreground">
          <SelectedIcon className="w-3 h-3" />
          <span>{PIECE_SET_NAMES[selectedPieceSet]}</span>
        </div>
      </div>
      <SegmentedControl
        options={pieceSetOptions}
        value={selectedPieceSet}
        onChange={(value) => setPieceSet(value as keyof typeof PIECE_SETS)}
        size="sm"
        className="w-full"
        iconOnly={true}
      />
    </div>
  );
}