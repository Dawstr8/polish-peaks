"use client";

import { PhotoClient } from "@/src/lib/clients/photo-client";
import { useMutation } from "@tanstack/react-query";
import { Spinner } from "@/src/components/ui/spinner";
import { PhotoPreview } from "@/src/app/upload/components/PhotoPreview";
import { Button } from "@/src/components/ui/button";
import { UploadSuccess } from "./UploadSuccess";

interface UploadStepProps {
  file: File;
  removeFile: () => void;
}

export function UploadStep({ file, removeFile }: UploadStepProps) {
  const mutation = useMutation({
    mutationFn: (file: File) => PhotoClient.uploadPhoto(file),
  });

  return (
    <div className="space-y-6">
      {mutation.isSuccess && <UploadSuccess />}
      {mutation.isError && (
        <div className="bg-destructive/10 border border-destructive/30 text-destructive px-4 py-3 rounded-lg">
          {mutation.error.message}
        </div>
      )}
      {!mutation.isSuccess && (
        <div className="flex flex-col gap-4 items-center justify-center">
          <PhotoPreview file={file} />
          <div className="flex gap-2">
            <Button
              onClick={() => mutation.mutate(file)}
              disabled={mutation.isPending}
            >
              {mutation.isPending && <Spinner />}
              {mutation.isPending ? "Uploading..." : "Upload Photo"}
            </Button>
            <Button variant="outline" onClick={removeFile}>
              Remove
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}
