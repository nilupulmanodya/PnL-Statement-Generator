import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";

export const Header = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    // Simple navigation without Supabase auth
    navigate("/");
  };

  return (
    <header className="fixed top-0 left-0 right-0 z-50">
      <div className="glass-card mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          <div className="flex-1 flex items-center justify-between">
            <div className="flex-shrink-0">
              <h1 className="text-xl font-semibold">CSE Reports</h1>
            </div>
            <Button
              variant="ghost"
              onClick={handleLogout}
              className="text-sm"
            >
              Sign out
            </Button>
          </div>
        </div>
      </div>
    </header>
  );
};