import { PhotoMetadataFormatter } from "./types";

const NOT_AVAILABLE = "N/A";

export class DefaultMetadataFormatter implements PhotoMetadataFormatter {
  formatLatitude(latitude?: number): string {
    return this.formatCoordinate(latitude);
  }

  formatLongitude(longitude?: number): string {
    return this.formatCoordinate(longitude);
  }

  formatAltitude(altitude?: number): string {
    if (altitude === undefined || altitude === null) return NOT_AVAILABLE;

    return `${altitude.toFixed(1)}m`;
  }

  formatCapturedAt(capturedAt?: string): string {
    if (!capturedAt) return NOT_AVAILABLE;

    try {
      const date = new Date(capturedAt);
      return date.toLocaleString();
    } catch {
      return NOT_AVAILABLE;
    }
  }

  private formatCoordinate(value?: number): string {
    if (value === undefined || value === null) return NOT_AVAILABLE;

    return `${value.toFixed(6)}°`;
  }
}

export function createMetadataFormatter(): PhotoMetadataFormatter {
  return new DefaultMetadataFormatter();
}
