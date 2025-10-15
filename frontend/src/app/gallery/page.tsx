"use client";

import { SummitPhotoCard } from "@/components/photos/SummitPhotoCard";
import { photoMetadataService } from "@/lib/metadata/service";
import { PhotoClient } from "@/lib/photos/client";
import { SummitPhoto } from "@/lib/photos/types";
import { useQuery } from "@tanstack/react-query";
import { Masonry } from "masonic";

export default function Gallery() {
  const { data: summitPhotos } = useQuery({
    queryKey: ["summitPhotos"],
    queryFn: async () => PhotoClient.getAllPhotos("captured_at", "desc"),
  });

  const renderCard = ({ data: summitPhoto }: { data: SummitPhoto }) => (
    <SummitPhotoCard
      key={summitPhoto.id}
      className="hover:shadow-lg hover:bg-gray-50 transition-all duration-200"
      summitPhoto={summitPhoto}
      formatter={photoMetadataService.getFormatter()}
    />
  );

  return (
    <div className="max-w-7xl mx-auto py-6 px-4 sm:px-6 lg:px-8">
      <Masonry
        items={summitPhotos || []}
        render={renderCard}
        columnWidth={300}
        columnGutter={16}
        rowGutter={16}
      />
    </div>
  );
}
