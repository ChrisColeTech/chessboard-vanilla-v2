import { usePageInstructions } from "../../hooks/core/usePageInstructions";
import { usePageData } from "../../hooks/core/usePageData";
import { ChessboardLayout } from "../../components/chess/ChessboardLayout";
import { DataTable } from "../../components/ui/DataTable";

export const SessionsPage = () => {
  usePageInstructions("sessions");
  const { data, loading, error } = usePageData("sessions");

  return (
    <div className="uitest-layout-container">
      <ChessboardLayout
        topLeft={<div className="uitest-layout-corner">Sessions Top Left</div>}
        top={<div className="uitest-layout-center"></div>}
        topRight={<div className="uitest-layout-corner">Sessions Top Right</div>}
        left={<div className="uitest-layout-corner">Sessions Left</div>}
        center={<DataTable data={data} loading={loading} error={error} />}
        right={<div className="uitest-layout-corner">Sessions Right</div>}
        bottomLeft={<div className="uitest-layout-corner">Sessions Bottom Left</div>}
        bottom={<div className="uitest-layout-center"></div>}
        bottomRight={<div className="uitest-layout-corner">Sessions Bottom Right</div>}
        className="w-full h-full"
      />
    </div>
  );
};
