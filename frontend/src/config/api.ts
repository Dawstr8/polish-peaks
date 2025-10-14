/**
 * API configuration
 * Centralized place for all API URLs and configuration
 */

/**
 * Base API URL
 * @description This is the base URL for all API requests
 */
export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api";

/**
 * API endpoints
 * @description These are the API endpoints used throughout the application
 */
export const API_ENDPOINTS = {
  photos: {
    post: `${API_BASE_URL}/photos`,
  },
  peaks: {
    find: (
      latitude: number,
      longitude: number,
      max_distance?: number,
      limit: number = 5,
    ) => {
      const params = new URLSearchParams({
        latitude: latitude.toString(),
        longitude: longitude.toString(),
        limit: limit.toString(),
      });

      if (max_distance !== undefined) {
        params.append("max_distance", max_distance.toString());
      }

      return `${API_BASE_URL}/peaks/find?${params.toString()}`;
    },
  },
} as const;
