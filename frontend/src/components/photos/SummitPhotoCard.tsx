"use client";

import Image from "next/image";
import { UPLOADS_BASE_URL } from "@/config/api";
import {
  Item,
  ItemContent,
  ItemDescription,
  ItemMedia,
  ItemTitle,
} from "@/components/ui/item";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { SummitPhoto } from "@/lib/photos/types";
import { ArrowUp, MapPin, Mountain } from "lucide-react";
import { PhotoMetadataFormatter } from "@/lib/metadata/types";
import { formatDistance } from "date-fns";

interface SummitPhotoCardProps {
  summitPhoto: SummitPhoto;
  formatter: PhotoMetadataFormatter;
  className?: string;
  uploadsBaseUrl?: string;
}

export function SummitPhotoCard({
  summitPhoto,
  formatter,
  className,
  uploadsBaseUrl = UPLOADS_BASE_URL,
}: SummitPhotoCardProps) {
  return (
    <Card className={className}>
      <CardHeader>
        <CardTitle>#{summitPhoto.id}</CardTitle>
        <CardDescription>
          {summitPhoto.captured_at &&
            formatDistance(new Date(summitPhoto.captured_at), new Date(), {
              addSuffix: true,
            })}
        </CardDescription>
      </CardHeader>

      <Image
        src={`${uploadsBaseUrl}${summitPhoto.file_name}`}
        alt={`Summit photo ${summitPhoto.id}`}
        width={1200}
        height={800}
        className="object-cover"
      />

      <CardContent className="space-y-4">
        {summitPhoto.altitude && (
          <Item className="p-0">
            <ItemMedia>
              <ArrowUp />
            </ItemMedia>
            <ItemContent>
              <ItemTitle className="text-base font-mono">
                {formatter.formatAltitude(summitPhoto.altitude)}
              </ItemTitle>
            </ItemContent>
          </Item>
        )}
        {summitPhoto.latitude && summitPhoto.longitude && (
          <Item className="p-0">
            <ItemMedia>
              <MapPin />
            </ItemMedia>
            <ItemContent>
              <ItemTitle className="text-base font-mono">
                {formatter.formatLatitude(summitPhoto.latitude)},{" "}
                {formatter.formatLongitude(summitPhoto.longitude)}
              </ItemTitle>
            </ItemContent>
          </Item>
        )}
        {summitPhoto.peak && (
          <Item className="p-0">
            <ItemMedia>
              <Mountain />
            </ItemMedia>
            <ItemContent>
              <ItemTitle className="text-base font-mono">
                {summitPhoto.peak.name}
              </ItemTitle>
              <ItemDescription className="flex justify-between w-full">
                <span>{summitPhoto.peak.range}</span>
                <span>
                  {formatter.formatAltitude(summitPhoto.peak.elevation)}
                </span>
              </ItemDescription>
            </ItemContent>
          </Item>
        )}
      </CardContent>
    </Card>
  );
}
