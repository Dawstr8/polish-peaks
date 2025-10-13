import { PhotoMetadata, PhotoMetadataFormatter } from "@/lib/metadata/types";
import { MapPin, Mountain, Clock } from "lucide-react";
import { MetadataItem } from "./MetadataItem";

interface MetadataDisplayProps {
  metadata: PhotoMetadata;
  formatter: PhotoMetadataFormatter;
}

export function MetadataDisplay({ metadata, formatter }: MetadataDisplayProps) {
  return (
    <div className="bg-muted/20 rounded-lg p-4 border border-border">
      <h4 className="text-lg font-semibold mb-4 text-foreground flex items-center gap-2">
        <MapPin className="h-5 w-5 text-primary" />
        Photo Metadata
      </h4>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        <MetadataItem
          icon={<MapPin />}
          label="Latitude"
          value={formatter.formatLatitude(metadata.latitude)}
        />
        <MetadataItem
          icon={<MapPin />}
          label="Longitude"
          value={formatter.formatLongitude(metadata.longitude)}
        />
        <MetadataItem
          icon={<Mountain />}
          label="Altitude"
          value={formatter.formatAltitude(metadata.altitude)}
        />
        <MetadataItem
          icon={<Clock />}
          label="Captured"
          value={formatter.formatCapturedAt(metadata.capturedAt)}
        />
      </div>
    </div>
  );
}
