"use client";

import { PhotoClient } from "@/lib/photos/client";
import { useMutation } from "@tanstack/react-query";
import { Spinner } from "@/components/ui/spinner";
import { PhotoPreview } from "@/components/upload/PhotoPreview";
import { Button } from "@/components/ui/button";
import { UploadSuccess } from "@/components/upload/UploadSuccess";
import { SummitPhotoCreate } from "@/lib/photos/types";

interface UploadStepProps {
  file: File | null;
  summitPhotoCreate: SummitPhotoCreate | null;
  back: () => void;
}

export function UploadStep({ file, summitPhotoCreate, back }: UploadStepProps) {
  const mutation = useMutation({
    mutationFn: ({
      file,
      summitPhotoCreate,
    }: {
      file: File;
      summitPhotoCreate: SummitPhotoCreate | null;
    }) => PhotoClient.uploadPhoto(file, summitPhotoCreate),
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
        <>
          <div className="flex items-center justify-center">
            <PhotoPreview file={file} />
          </div>
          <div className="flex justify-center gap-4">
            <Button variant="outline" onClick={back}>
              Back
            </Button>
            <Button
              onClick={() =>
                file && mutation.mutate({ file, summitPhotoCreate })
              }
              disabled={mutation.isPending}
            >
              {mutation.isPending && <Spinner />}
              {mutation.isPending ? "Uploading..." : "Upload Photo"}
            </Button>
          </div>
        </>
      )}
    </div>
  );
}
