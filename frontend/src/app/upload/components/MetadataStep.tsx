"use client";

import { Button } from "@/components/ui/button";
import { MetadataDisplay } from "@/app/upload/components/MetadataDisplay";
import { PhotoMetadata } from "@/lib/metadata/types";
import { photoMetadataService } from "@/lib/metadata/service";
import { SummitPhotoCreate } from "@/lib/photos/types";
import { mapPhotoMetadataToSummitPhotoCreate } from "@/lib/photos/mappers";

interface MetadataStepProps {
  file: File | null;
  metadata: PhotoMetadata;
  setSummitPhotoCreate: (summitPhotoCreate: SummitPhotoCreate) => void;
  back: () => void;
  next: () => void;
}

export function MetadataStep({
  metadata,
  setSummitPhotoCreate,
  back,
  next,
}: MetadataStepProps) {
  const handleAccept = () => {
    const summitPhotoCreate = mapPhotoMetadataToSummitPhotoCreate(metadata);
    setSummitPhotoCreate(summitPhotoCreate);
    next();
  };

  return (
    <div className="space-y-6">
      <MetadataDisplay
        metadata={metadata}
        formatter={photoMetadataService.getFormatter()}
      />
      <div className="flex justify-center gap-4">
        <Button variant="outline" onClick={back}>
          Back
        </Button>
        <Button onClick={handleAccept}>Accept</Button>
      </div>
    </div>
  );
}
