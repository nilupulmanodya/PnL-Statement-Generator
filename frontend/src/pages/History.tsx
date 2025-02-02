import { Header } from "@/components/layout/Header";
import { HistoryTable } from "@/components/dashboard/HistoryTable";
import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";
import { Upload } from "lucide-react";

const History = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
      <Header />
      <main className="container mx-auto px-4 pt-24 pb-12">
        <div className="max-w-4xl mx-auto space-y-8">
          <div className="flex justify-between items-center">
            <h2 className="text-3xl font-semibold tracking-tight">Report History</h2>
            <Button
              variant="outline"
              onClick={() => navigate("/dashboard")}
              className="flex items-center gap-2"
            >
              <Upload className="w-4 h-4" />
              Upload New
            </Button>
          </div>
          <HistoryTable />
        </div>
      </main>
    </div>
  );
};

export default History;