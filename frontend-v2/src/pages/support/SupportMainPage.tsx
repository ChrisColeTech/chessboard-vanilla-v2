import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { usePageData } from "../../hooks/core/usePageData";
import { ChessboardLayout } from "../../components/chess/ChessboardLayout";
import { DataTable } from "../../components/ui/DataTable";

export const SupportMainPage = () => {
  usePageInstructions("support");
  const { data, loading, error } = usePageData("support");

  return (
    <div className="uitest-layout-container">
      <ChessboardLayout
        topLeft={<div className="uitest-layout-corner">Support Main Top Left</div>}
        top={<div className="uitest-layout-center"></div>}
        topRight={<div className="uitest-layout-corner">Support Main Top Right</div>}
        left={<div className="uitest-layout-corner">Support Main Left</div>}
        center={<DataTable data={data} loading={loading} error={error} />}
        right={<div className="uitest-layout-corner">Support Main Right</div>}
        bottomLeft={<div className="uitest-layout-corner">Support Main Bottom Left</div>}
        bottom={<div className="uitest-layout-center"></div>}
        bottomRight={<div className="uitest-layout-corner">Support Main Bottom Right</div>}
        className="w-full h-full"
      />
    </div>
  );
};
