import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { usePageData } from "../../hooks/core/usePageData";
import { MobileChessboardLayout } from "../../components/chess/MobileChessboardLayout";
import { DataTable } from "../../components/ui/DataTable";

export const MobileAnalysisPage = () => {
  usePageInstructions("analysis");
  const { data, loading, error } = usePageData("analysis");

  return (
    <div className="uitest-mobile-container-padded">
      <MobileChessboardLayout
        topPieces={<div className="uitest-mobile-pieces">Analysis Top Pieces</div>}
        center={<DataTable data={data} loading={loading} error={error} />}
        bottomPieces={<div className="uitest-mobile-pieces">Analysis Bottom Pieces</div>}
      />
    </div>
  );
};
