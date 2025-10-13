"use client";

import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { Upload } from "lucide-react";
import { useDropzone } from "react-dropzone";

interface PhotoDropzoneProps {
  onSelect: (file: File) => void;
}

export function PhotoDropzone({ onSelect }: PhotoDropzoneProps) {
  const onDrop = (acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (!file) return;

    onSelect(file);
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { "image/*": [] },
    multiple: false,
  });

  return (
    <div
      {...getRootProps()}
      className={cn(
        "border-2 border-dashed rounded-lg p-12 flex flex-col items-center justify-center cursor-pointer transition-colors",
        isDragActive ? "border-primary bg-primary/10" : "border-border",
      )}
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
      <Button>Select File</Button>
      <input {...getInputProps()} />
    </div>
  );
}
