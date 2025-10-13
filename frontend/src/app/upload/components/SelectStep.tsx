"use client";

import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { Upload } from "lucide-react";
import { useDropzone } from "react-dropzone";
import { photoMetadataService } from "@/lib/metadata/service";
import { PhotoMetadata } from "@/lib/metadata/types";
import { useMutation } from "@tanstack/react-query";
import { Spinner } from "@/components/ui/spinner";

interface SelectStepProps {
  setFile: (file: File) => void;
  setMetadata: (metadata: PhotoMetadata) => void;
  next: () => void;
}

export function SelectStep({ setFile, setMetadata, next }: SelectStepProps) {
  const mutation = useMutation({
    mutationFn: (file: File) => photoMetadataService.extractMetadata(file),
    onSuccess: (metadata) => {
      setMetadata(metadata);
    },
    onSettled: (metadata, error, file) => {
      setFile(file);
      next();
    },
  });

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop: (acceptedFiles: File[]) => {
      const file = acceptedFiles[0];
      if (!file) return;

      mutation.mutate(file);
    },
    accept: { "image/*": [] },
    multiple: false,
    disabled: mutation.isPending,
  });

  return (
    <div
      {...getRootProps()}
      className={cn(
        "border-2 border-dashed rounded-lg p-12 flex flex-col items-center justify-center cursor-pointer transition-colors",
        isDragActive ? "border-primary bg-primary/10" : "border-border",
        mutation.isPending && "opacity-50 cursor-not-allowed",
      )}
    >
      <div className="p-4 mb-4 bg-secondary rounded-full">
        <Upload className="w-10 h-10 text-primary" />
      </div>
      <h3 className="text-lg font-semibold mb-2 text-foreground">
        {mutation.isPending
          ? "Extracting metadata..."
          : "Drag and drop or click to upload"}
      </h3>
      <p className="text-sm text-muted-foreground mb-4">
        Support for JPG, PNG files. Metadata will be extracted automatically.
      </p>
      <Button disabled={mutation.isPending}>
        {mutation.isPending && <Spinner />}
        {mutation.isPending ? "Processing..." : "Select File"}
      </Button>
      <input {...getInputProps()} />
    </div>
  );
}
