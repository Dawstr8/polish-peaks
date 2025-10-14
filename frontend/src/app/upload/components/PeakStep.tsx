"use client";

import { useState } from "react";
import { useQuery } from "@tanstack/react-query";
import { Button } from "@/components/ui/button";
import { PeakClient } from "@/lib/peaks/client";
import { PeakWithDistance } from "@/lib/peaks/types";
import { SummitPhotoCreate } from "@/lib/photos/types";
import { PeakSelect } from "./PeaksSelect";

const MAX_DISTANCE = 10000; // 10 km
const LIMIT = 6;

interface PeakStepProps {
  summitPhotoCreate: SummitPhotoCreate | null;
  setSummitPhotoCreate: (summitPhotoCreate: SummitPhotoCreate) => void;
  back: () => void;
  next: () => void;
}

export function PeakStep({
  summitPhotoCreate,
  setSummitPhotoCreate,
  back,
  next,
}: PeakStepProps) {
  const [selectedPeakId, setSelectedPeakId] = useState<number | null>(null);
  const { latitude, longitude } = summitPhotoCreate || {};

  const {
    data: peaksWithDistance,
    isLoading,
    error,
  } = useQuery({
    queryKey: ["nearby-peaks", latitude, longitude],
    queryFn: () =>
      PeakClient.findNearbyPeaks(latitude!, longitude!, MAX_DISTANCE, LIMIT),
    enabled: !!latitude && !!longitude,
  });

  const handleSelect = ({ peak, distance }: PeakWithDistance) => {
    setSelectedPeakId(peak.id);

    setSummitPhotoCreate({
      ...summitPhotoCreate,
      peak_id: peak.id,
      distance_to_peak: distance,
    });
  };

  return (
    <div className="space-y-6">
      <div className="text-center">
        <h3 className="text-lg font-semibold mb-2">Select a Peak</h3>
        <p className="text-muted-foreground">
          Choose the peak this photo was taken near. This helps organize your
          mountain adventures.
        </p>
      </div>

      <PeakSelect
        peaksWithDistance={peaksWithDistance || []}
        isLoading={isLoading}
        error={error}
        selectedId={selectedPeakId}
        onSelect={handleSelect}
      />

      <div className="flex justify-center gap-4">
        <Button variant="outline" onClick={back}>
          Back
        </Button>
        <Button onClick={next} size="lg">
          Confirm Peak Selection
        </Button>
      </div>
    </div>
  );
}
