/**
 * API client for interacting with the photo endpoints
 */

import { SummitPhoto } from "@/src/lib/photos/model";
import { API_ENDPOINTS } from "@/src/config/api";
import { ApiClient } from "../common/api-client";

/**
 * PhotoClient class for handling photo-related API requests
 */
export class PhotoClient extends ApiClient {
  /**
   * Upload a photo file to the backend
   * @param file The file to upload
   * @returns The uploaded photo data
   * @throws Error if the upload fails
   */
  static async uploadPhoto(file: File): Promise<SummitPhoto> {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("summit_photo_create", "{}");

    return this.post<SummitPhoto>(API_ENDPOINTS.photos.post, formData);
  }
}
