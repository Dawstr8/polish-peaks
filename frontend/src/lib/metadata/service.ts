import {
  PhotoMetadata,
  PhotoMetadataExtractor,
  PhotoMetadataFormatter,
} from "./types";
import { createMetadataExtractor } from "./extractor";
import { createMetadataFormatter } from "./formatter";

export class PhotoMetadataService {
  constructor(
    private extractor: PhotoMetadataExtractor = createMetadataExtractor(),
    private formatter: PhotoMetadataFormatter = createMetadataFormatter(),
  ) {}

  async extractMetadata(file: File): Promise<PhotoMetadata> {
    return this.extractor.extract(file);
  }

  getFormatter(): PhotoMetadataFormatter {
    return this.formatter;
  }
}

export const photoMetadataService = new PhotoMetadataService();
