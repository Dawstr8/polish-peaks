"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Upload } from "lucide-react";
import { SelectStep } from "@/app/upload/components/SelectStep";
import { UploadStep } from "./components/UploadStep";
import { useStepper } from "@/hooks/use-stepper";
import { MetadataStep } from "./components/MetadataStep";
import { PhotoMetadata } from "@/lib/metadata/types";
import { SummitPhotoCreate } from "@/lib/photos/types";
import { PeakStep } from "./components/PeakStep";

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [metadata, setMetadata] = useState<PhotoMetadata>({});
  const [summitPhotoCreate, setSummitPhotoCreate] =
    useState<SummitPhotoCreate | null>(null);
  const { step, next, back } = useStepper(4);

  const renderStep = () => {
    switch (step) {
      case 0:
        return (
          <SelectStep setFile={setFile} setMetadata={setMetadata} next={next} />
        );
      case 1:
        return (
          <MetadataStep
            metadata={metadata}
            setSummitPhotoCreate={setSummitPhotoCreate}
            back={back}
            next={next}
          />
        );
      case 2:
        return (
          <PeakStep
            summitPhotoCreate={summitPhotoCreate}
            setSummitPhotoCreate={setSummitPhotoCreate}
            back={back}
            next={next}
          />
        );
      case 3:
        return (
          <UploadStep
            file={file}
            summitPhotoCreate={summitPhotoCreate}
            back={back}
          />
        );
      default:
        return null;
    }
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
        <CardContent>{renderStep()}</CardContent>
      </Card>
    </div>
  );
}
