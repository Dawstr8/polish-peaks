import { PhotoMetadata } from "../metadata/types";
import { SummitPhotoCreate } from "./types";

/**
 * Converts PhotoMetadata to SummitPhotoCreate
 * @param metadata The extracted photo metadata
 * @returns SummitPhotoCreate object
 */
export function mapPhotoMetadataToSummitPhotoCreate(
  metadata: PhotoMetadata,
): SummitPhotoCreate {
  return {
    captured_at: metadata.capturedAt,
    latitude: metadata.latitude,
    longitude: metadata.longitude,
    altitude: metadata.altitude,
  };
}
