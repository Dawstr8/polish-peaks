"use client";

import { PhotoClient } from "@/lib/photos/client";
import { useMutation } from "@tanstack/react-query";
import { Spinner } from "@/components/ui/spinner";
import { Button } from "@/components/ui/button";
import { UploadSuccess } from "@/components/upload/UploadSuccess";
import { SummitPhoto, SummitPhotoCreate } from "@/lib/photos/types";
import { SummitPhotoCard } from "@/components/photos/SummitPhotoCard";
import { photoMetadataService } from "@/lib/metadata/service";
import { Peak } from "@/lib/peaks/types";

interface UploadStepProps {
  file: File;
  summitPhotoCreate: SummitPhotoCreate;
  selectedPeak: Peak | null;
  back: () => void;
}

export function UploadStep({
  file,
  summitPhotoCreate,
  selectedPeak,
  back,
}: UploadStepProps) {
  const { isPending, isSuccess, isError, error, mutate } = useMutation({
    mutationFn: ({
      file,
      summitPhotoCreate,
    }: {
      file: File;
      summitPhotoCreate: SummitPhotoCreate | null;
    }) => PhotoClient.uploadPhoto(file, summitPhotoCreate),
  });

  if (isSuccess) {
    return <UploadSuccess />;
  }

  if (isError) {
    return (
      <div className="bg-destructive/10 border border-destructive/30 text-destructive px-4 py-3 rounded-lg">
        {error.message}
      </div>
    );
  }

  const summitPhoto = {
    ...summitPhotoCreate,
    file_name: URL.createObjectURL(file),
    uploaded_at: new Date().toISOString(),
    id: 999,
    peak: selectedPeak,
  } as unknown as SummitPhoto;

  return (
    <div className="space-y-6">
      <SummitPhotoCard
        summitPhoto={summitPhoto}
        formatter={photoMetadataService.getFormatter()}
        uploadsBaseUrl=""
        className="max-w-1/2 mx-auto"
      />
      <div className="flex justify-center gap-4">
        <Button variant="outline" onClick={back}>
          Back
        </Button>
        <Button
          onClick={() => file && mutate({ file, summitPhotoCreate })}
          disabled={isPending}
        >
          {isPending && <Spinner />}
          {isPending ? "Uploading..." : "Upload Photo"}
        </Button>
      </div>
    </div>
  );
}
