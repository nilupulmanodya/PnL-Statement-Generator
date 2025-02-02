import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { Button } from "@/components/ui/button";
import { useToast } from "@/components/ui/use-toast";
import { Upload } from "lucide-react";

export const FileUpload = () => {
  const [dragging, setDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const { toast } = useToast();
  const navigate = useNavigate();

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragging(true);
    } else if (e.type === "dragleave") {
      setDragging(false);
    }
  };

  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragging(false);
    
    const files = e.dataTransfer.files;
    if (files && files[0]) {
      await handleUpload(files[0]);
    }
  };

  const handleFileSelect = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files[0]) {
      await handleUpload(files[0]);
    }
  };

  const handleUpload = async (file: File) => {
    if (file.type !== "application/pdf") {
      toast({
        title: "Invalid file type",
        description: "Please upload a PDF file",
        variant: "destructive",
      });
      return;
    }

    setUploading(true);

    // Simulate upload delay
    await new Promise(resolve => setTimeout(resolve, 2000));

    try {
      toast({
        title: "Success",
        description: "Report uploaded successfully",
      });

      navigate("/history");
    } catch (error: any) {
      toast({
        title: "Error",
        description: error.message,
        variant: "destructive",
      });
    } finally {
      setUploading(false);
    }
  };

  return (
    <div
      className={`glass-card p-8 rounded-2xl transition-all duration-200 ${
        dragging ? "border-primary" : ""
      }`}
      onDragEnter={handleDrag}
      onDragLeave={handleDrag}
      onDragOver={handleDrag}
      onDrop={handleDrop}
    >
      <div className="text-center space-y-4">
        <div className="mx-auto w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
          <Upload className="w-6 h-6 text-primary" />
        </div>
        <div>
          <h3 className="text-lg font-semibold">Upload CSE Statement</h3>
          <p className="text-sm text-muted-foreground mt-1">
            Drag and drop your PDF file here, or click to select
          </p>
        </div>
        <div className="relative">
          <input
            type="file"
            accept=".pdf"
            onChange={handleFileSelect}
            className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            disabled={uploading}
          />
          <Button disabled={uploading} className="w-full">
            {uploading ? "Uploading..." : "Select File"}
          </Button>
        </div>
      </div>
    </div>
  );
};