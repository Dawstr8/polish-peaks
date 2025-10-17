/**
 * API client for interacting with the photo endpoints
 */
import { API_BASE_URL, API_ENDPOINTS } from "@/config/api";
import { ApiClient } from "@/lib/common/api-client";
import { PeakWithDistance } from "./types";

/**
 * PeakClient class for handling peak-related API requests
 */
export class PeakClient extends ApiClient {
  protected static getInstance() {
    return super.getInstance(`${API_BASE_URL}/${API_ENDPOINTS.PEAKS}`);
  }

  /**
   * Find nearby peaks based on latitude and longitude
   * @param latitude The latitude of the location
   * @param longitude The longitude of the location
   * @param max_distance The maximum distance in meters to search for peaks (optional)
   * @param limit The maximum number of peaks to return (default is 5)
   * @returns A list of nearby peaks with their distances
   * @throws Error if the request fails
   */
  static async findNearbyPeaks(
    latitude: number,
    longitude: number,
    max_distance?: number,
    limit: number = 5,
  ): Promise<PeakWithDistance[]> {
    return this.get<PeakWithDistance[]>("/find", {
      params: {
        latitude,
        longitude,
        max_distance,
        limit,
      },
    });
  }
}
