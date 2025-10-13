export interface PhotoMetadata {
  latitude?: number;
  longitude?: number;
  altitude?: number;
  capturedAt?: string; // ISO string
}

export interface PhotoMetadataExtractor {
  extract(file: File): Promise<PhotoMetadata>;
}

export interface PhotoMetadataFormatter {
  formatLatitude(latitude?: number): string;
  formatLongitude(longitude?: number): string;
  formatAltitude(altitude?: number): string;
  formatCapturedAt(capturedAt?: string): string;
}
