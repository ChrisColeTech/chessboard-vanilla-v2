import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { usePageData } from "../../hooks/core/usePageData";
import { MobileChessboardLayout } from "../../components/chess/MobileChessboardLayout";
import { DataTable } from "../../components/ui/DataTable";

export const MobileStatsPage = () => {
  usePageInstructions("stats");
  const { data, loading, error } = usePageData("stats");

  return (
    <div className="uitest-mobile-container-padded">
      <MobileChessboardLayout
        topPieces={<div className="uitest-mobile-pieces">Stats Top Pieces</div>}
        center={<DataTable data={data} loading={loading} error={error} />}
        bottomPieces={<div className="uitest-mobile-pieces">Stats Bottom Pieces</div>}
      />
    </div>
  );
};
