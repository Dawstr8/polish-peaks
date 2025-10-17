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
  process.env.NEXT_PUBLIC_UPLOADS_BASE_URL || "http://localhost:8000/uploads/";

/**
 * API endpoints
 * @description These are the API endpoints used throughout the application
 */
export const API_ENDPOINTS = {
  PHOTOS: "photos",
  PEAKS: "peaks",
} as const;
