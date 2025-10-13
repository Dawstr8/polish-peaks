"use client";

import { Button } from "@/src/components/ui/button";
import { cn } from "@/src/lib/utils";
import { Upload } from "lucide-react";
import { useState } from "react";

interface PhotoDropzoneProps {
  onSelect: (file: File) => void;
}

export function PhotoDropzone({ onSelect }: PhotoDropzoneProps) {
  const [isDragActive, setIsDragActive] = useState(false);

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragActive(false);

    if (!e.dataTransfer.files || e.dataTransfer.files.length === 0) {
      return;
    }

    onSelect(e.dataTransfer.files[0]);
    e.dataTransfer.clearData();
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragActive(true);
  };

  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragActive(false);
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) {
      return;
    }

    onSelect(e.target.files[0]);
  };

  const handleClick = () => {
    document.getElementById("file-upload")?.click();
  };

  return (
    <div
      className={cn(
        "border-2 border-dashed rounded-lg p-12 flex flex-col items-center justify-center",
        isDragActive ? "border-primary bg-primary/10" : "border-border",
      )}
      onClick={handleClick}
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      tabIndex={0}
      role="button"
      aria-label="Upload photo"
    >
      <div className="p-4 mb-4 bg-secondary rounded-full">
        <Upload className="w-10 h-10 text-primary" />
      </div>
      <h3 className="text-lg font-semibold mb-2 text-foreground">
        Drag and drop or click to upload
      </h3>
      <p className="text-sm text-muted-foreground mb-4">
        Support for JPG, PNG files.
      </p>
      <Button type="button" onClick={(e) => e.preventDefault()}>
        Select File
      </Button>
      <input
        id="file-upload"
        type="file"
        accept="image/*"
        onChange={handleFileChange}
        className="hidden"
      />
    </div>
  );
}
