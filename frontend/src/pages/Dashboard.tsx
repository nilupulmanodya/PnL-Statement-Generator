import { Header } from "@/components/layout/Header";
import { FileUpload } from "@/components/dashboard/FileUpload";
import { Button } from "@/components/ui/button";
import { useNavigate } from "react-router-dom";
import { History } from "lucide-react";

const Dashboard = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
      <Header />
      <main className="container mx-auto px-4 pt-24 pb-12">
        <div className="max-w-4xl mx-auto space-y-8">
          <div className="flex justify-between items-center">
            <h2 className="text-3xl font-semibold tracking-tight">Dashboard</h2>
            <Button
              variant="outline"
              onClick={() => navigate("/history")}
              className="flex items-center gap-2"
            >
              <History className="w-4 h-4" />
              View History
            </Button>
          </div>
          <FileUpload />
        </div>
      </main>
    </div>
  );
};

export default Dashboard;