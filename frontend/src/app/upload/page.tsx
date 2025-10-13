"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Upload } from "lucide-react";
import { PhotoDropzone } from "@/app/upload/components/PhotoDropzone";
import { UploadStep } from "./components/UploadStep";

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);

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
          {file ? (
            <UploadStep file={file} removeFile={() => setFile(null)} />
          ) : (
            <PhotoDropzone onSelect={setFile} />
          )}
        </CardContent>
      </Card>
    </div>
  );
}
