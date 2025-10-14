"use client";

import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { Upload } from "lucide-react";
import { useDropzone } from "react-dropzone";
import { photoMetadataService } from "@/lib/metadata/service";
import { PhotoMetadata } from "@/lib/metadata/types";
import { useMutation } from "@tanstack/react-query";
import { Spinner } from "@/components/ui/spinner";
import { MessageBlock } from "@/components/common/MessageBlock";

interface SelectStepProps {
  setFile: (file: File) => void;
  setMetadata: (metadata: PhotoMetadata) => void;
  next: () => void;
}

export function SelectStep({ setFile, setMetadata, next }: SelectStepProps) {
  const { mutate, isPending } = useMutation({
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

      mutate(file);
    },
    accept: { "image/*": [] },
    multiple: false,
    disabled: isPending,
  });

  return (
    <div
      {...getRootProps()}
      className={cn(
        "border-2 border-dashed rounded-lg p-12 flex flex-col items-center justify-center cursor-pointer transition-colors",
        isDragActive ? "border-primary bg-primary/10" : "border-border",
        isPending && "opacity-50 cursor-not-allowed",
      )}
    >
      <MessageBlock
        iconComponent={Upload}
        title={
          isPending
            ? "Extracting metadata..."
            : "Drag and drop or click to upload"
        }
        description="Support for JPG, PNG files. Metadata will be extracted automatically."
        className="mb-4"
      />

      <Button disabled={isPending}>
        {isPending && <Spinner />}
        {isPending ? "Processing..." : "Select File"}
      </Button>
      <input {...getInputProps()} />
    </div>
  );
}
