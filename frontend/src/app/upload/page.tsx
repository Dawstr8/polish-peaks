"use client";

import { useState } from "react";
import { Button } from "@/src/components/ui/button";
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/src/components/ui/card";
import { Upload } from "lucide-react";
import { PhotoClient } from "@/src/lib/clients/photo-client";
import { Spinner } from "@/src/components/ui/spinner";
import { UploadSuccess } from "@/src/app/upload/components/UploadSuccess";
import { PhotoPreview } from "@/src/app/upload/components/PhotoPreview";
import { PhotoDropzone } from "@/src/app/upload/components/PhotoDropzone";
import { useMutation } from "@tanstack/react-query";

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const mutation = useMutation({
    mutationFn: (file: File) => PhotoClient.uploadPhoto(file),
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;

    mutation.mutate(file);
  };

  const changeFile = (newFile: File | null) => {
    setFile(newFile);
    mutation.reset();
  };

  return (
    <div className="container py-10 mx-auto">
      <h1 className="text-3xl font-bold mb-8 text-center text-primary">
        Upload Summit Photo
      </h1>

      <Card className="max-w-3xl mx-auto shadow-md border-border">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Upload className="h-6 w-6" />
            <span>Share Your Mountain Adventure</span>
          </CardTitle>
        </CardHeader>
        <CardContent>
          {mutation.isSuccess ? (
            <UploadSuccess />
          ) : (
            <form onSubmit={handleSubmit} className="space-y-6">
              {!file && <PhotoDropzone onSelect={changeFile} />}

              {mutation.isError && (
                <div className="bg-destructive/10 border border-destructive/30 text-destructive px-4 py-3 rounded-lg">
                  {mutation.error.message}
                </div>
              )}

              {file && (
                <div className="flex flex-col gap-4 items-center justify-center">
                  <PhotoPreview file={file} />
                  <div className="flex gap-2">
                    <Button type="submit" disabled={mutation.isPending}>
                      {mutation.isPending && <Spinner />}
                      {mutation.isPending ? "Uploading..." : "Upload Photo"}
                    </Button>
                    <Button
                      type="button"
                      variant="outline"
                      onClick={() => changeFile(null)}
                    >
                      Remove
                    </Button>
                  </div>
                </div>
              )}
            </form>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
