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

export const UPLOADS_BASE_URL =
  process.env.NEXT_PUBLIC_UPLOADS_BASE_URL || "http://localhost:8000/uploads";

/**
 * API endpoints
 * @description These are the API endpoints used throughout the application
 */
export const API_ENDPOINTS = {
  photos: {
    getAll: (
      sort_by: string | null = null,
      order: "asc" | "desc" | null = null,
    ) => {
      const params = new URLSearchParams();

      if (sort_by) {
        params.append("sort_by", sort_by);
      }

      if (order) {
        params.append("order", order);
      }

      return `${API_BASE_URL}/photos?${params.toString()}`;
    },
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
