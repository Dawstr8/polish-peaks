/**
 * API client for interacting with the photo endpoints
 */

import { SummitPhoto, SummitPhotoCreate } from "@/lib/photos/types";
import { API_ENDPOINTS } from "@/config/api";
import { ApiClient } from "@/lib/common/api-client";

/**
 * PhotoClient class for handling photo-related API requests
 */
export class PhotoClient extends ApiClient {
  /**
   * Get all summit photos from the backend
   * @param sortBy Optional field to sort by
   * @param order Optional order of sorting (asc or desc)
   * @returns A list of all summit photos
   * @throws Error if the request fails
   */
  static async getAllPhotos(
    sortBy: string | null = null,
    order: "asc" | "desc" | null = null,
  ): Promise<SummitPhoto[]> {
    return this.get<SummitPhoto[]>(API_ENDPOINTS.photos.getAll(sortBy, order));
  }

  /**
   * Upload a photo file to the backend
   * @param file The file to upload
   * @returns The uploaded photo data
   * @throws Error if the upload fails
   */
  static async uploadPhoto(
    file: File,
    summitPhotoCreate: SummitPhotoCreate | null,
  ): Promise<SummitPhoto> {
    const formData = new FormData();
    formData.append("file", file);
    formData.append(
      "summit_photo_create",
      summitPhotoCreate ? JSON.stringify(summitPhotoCreate) : "",
    );

    return this.post<SummitPhoto>(API_ENDPOINTS.photos.post, formData);
  }
}
