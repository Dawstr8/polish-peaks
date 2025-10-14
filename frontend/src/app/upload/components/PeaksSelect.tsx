import { AlertCircleIcon, Ruler, SearchX } from "lucide-react";
import { PeakWithDistance } from "@/lib/peaks/types";
import { Spinner } from "@/components/ui/spinner";
import { Badge } from "@/components/ui/badge";
import { Alert, AlertDescription, AlertTitle } from "@/components/ui/alert";
import { PeakCard } from "@/components/peaks/PeakCard";
import { cn } from "@/lib/utils";

interface PeakSelectProps {
  peaksWithDistance: PeakWithDistance[];
  isLoading: boolean;
  error: Error | null;
  selectedId: number | null;
  onSelect: (peakWithDistance: PeakWithDistance) => void;
}

export function PeakSelect({
  peaksWithDistance,
  isLoading,
  error,
  selectedId,
  onSelect,
}: PeakSelectProps) {
  if (isLoading) {
    return (
      <div className="flex items-center justify-center py-8 gap-2">
        <Spinner className="size-8" />
        <span className="text-muted-foreground">Finding nearby peaks...</span>
      </div>
    );
  }

  if (error) {
    return (
      <Alert variant="destructive">
        <AlertCircleIcon />
        <AlertTitle>Error Loading Peaks</AlertTitle>
        <AlertDescription>
          Failed to load nearby peaks. Please try again later.
        </AlertDescription>
      </Alert>
    );
  }

  if (!peaksWithDistance || peaksWithDistance.length === 0) {
    return (
      <Alert>
        <SearchX />
        <AlertTitle>No Peaks Found</AlertTitle>
        <AlertDescription>
          No peaks found near this location. You can still proceed without
          assigning a peak.
        </AlertDescription>
      </Alert>
    );
  }

  return (
    <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
      {peaksWithDistance.map(({ peak, distance }) => {
        const isHighlighted = selectedId === peak.id;
        return (
          <PeakCard
            key={peak.id}
            peak={peak}
            className={cn(
              "cursor-pointer transition-all hover:bg-accent/5",
              isHighlighted &&
                "ring-2 ring-primary border-primary bg-accent/10",
            )}
            onClick={() => onSelect({ peak, distance })}
          >
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Ruler className="h-3 w-3" />
              <span>{distance.toFixed(1)}m away</span>
            </div>
            <Badge
              variant={isHighlighted ? "default" : "secondary"}
              className="w-full justify-center mt-2"
            >
              {isHighlighted ? "Selected" : "Select"}
            </Badge>
          </PeakCard>
        );
      })}
    </div>
  );
}
