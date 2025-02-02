import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { Toaster } from "@/components/ui/toaster";
import Dashboard from "./pages/Dashboard";
import History from "./pages/History";
import NotFound from "./pages/NotFound";

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/dashboard"
          element={
              <Dashboard />
          }
        />
        <Route
          path="/history"
          element={
              <History />
          }
        />
        <Route path="*" element={<NotFound />} />
      </Routes>
      <Toaster />
    </BrowserRouter>
  );
};

export default App;