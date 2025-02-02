import { useState } from "react";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Button } from "@/components/ui/button";
import { Download } from "lucide-react";
import { supabase } from "@/lib/supabase";
import { useEffect } from "react";

type Report = {
  id: string;
  created_at: string;
  status: "pending" | "success" | "error";
  cse_report: string;
  pl_report: string | null;
};

export const HistoryTable = () => {
  const [loading] = useState(false);
  const [reports, setReports] = useState<Report[]>([]);
  
  useEffect(() => {
    const fetchReports = async () => {
      const { data, error } = await supabase
        .from('table')
        .select('*')
        .order('created_at', { ascending: false });

      if (error) {
        console.error('Error fetching reports:', error);
      } else {
        setReports(data);
      }
    };

    fetchReports();

    // Subscribe to real-time changes
    const subscription = supabase
      .channel('reports-realtime')
      .on(
        'postgres_changes', 
        { event: '*', schema: 'public', table: 'table' }, 
        (payload) => {
          console.log('Change received:', payload);

          if (payload.eventType === 'INSERT') {
            setReports((prevReports) => [(payload.new as Report), ...prevReports]);
          } else if (payload.eventType === 'UPDATE') {
            setReports((prevReports) =>
              prevReports.map((report) =>
                report.id === payload.new.id ? (payload.new as Report) : report
              )
            );
          } else if (payload.eventType === 'DELETE') {
            setReports((prevReports) =>
              prevReports.filter((report) => report.id !== payload.old.id)
            );
          }
        }
      )
      .subscribe();

    return () => {
      supabase.removeChannel(subscription); // Cleanup subscription on unmount
    };
  }, []);

  const getStatusBadgeClass = (status: Report["status"]) => {
    const baseClasses = "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium";
    switch (status) {
      case "success":
        return `${baseClasses} bg-green-100 text-green-800`;
      case "error":
        return `${baseClasses} bg-red-100 text-red-800`;
      default:
        return `${baseClasses} bg-yellow-100 text-yellow-800`;
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-pulse">Loading...</div>
      </div>
    );
  }

  if (reports.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-muted-foreground">No reports available</p>
      </div>
    );
  }

  return (
    <div className="glass-card rounded-2xl overflow-hidden">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Created At</TableHead>
            <TableHead>Status</TableHead>
            <TableHead>CSE Report</TableHead>
            <TableHead>PnL Report</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {reports.map((report) => (
            <TableRow key={report.id}>
              <TableCell>
                {new Date(report.created_at).toLocaleDateString()}
              </TableCell>
              <TableCell>
                <span className={getStatusBadgeClass(report.status)}>
                  {report.status.charAt(0).toUpperCase() + report.status.slice(1)}
                </span>
              </TableCell>
              <TableCell>
                {report.cse_report && (
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => window.open(report.cse_report, "_blank")}
                  >
                    <Download className="w-4 h-4 mr-2" />
                    Download
                  </Button>
                )}
              </TableCell>
              <TableCell>
                {report.pl_report && (
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => window.open(report.pl_report, "_blank")}
                  >
                    <Download className="w-4 h-4 mr-2" />
                    Download
                  </Button>
                )}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
};