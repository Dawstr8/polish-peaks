"use client";

import Image from "next/image";

interface PhotoPreviewProps {
  file: File;
}

export function PhotoPreview({ file }: PhotoPreviewProps) {
  return (
    <div className="relative w-60 h-40 overflow-hidden rounded-lg">
      <Image
        src={URL.createObjectURL(file)}
        alt="Preview"
        fill
        style={{ objectFit: "cover" }}
        className="rounded-lg"
      />
    </div>
  );
}
