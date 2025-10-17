/**
 * Base API client class for making HTTP requests to the backend
 */

import axios, { AxiosInstance, AxiosError } from "axios";
import { API_BASE_URL } from "@/config/api";

/**
 * Error response from the API
 */
interface ApiErrorResponse {
  message?: string;
  errors?: Record<string, string[]>;
  [key: string]: unknown;
}

/**
 * Base API client class
 */
export class ApiClient {
  private static instance: AxiosInstance;

  protected static getInstance(baseUrl: string = API_BASE_URL): AxiosInstance {
    if (!this.instance) {
      this.instance = axios.create({
        baseURL: baseUrl,
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
      });

      this.instance.interceptors.response.use(
        (response) => response,
        (error: AxiosError) => {
          return Promise.reject(this.handleError(error));
        },
      );
    }
    return this.instance;
  }

  /**
   * Handles API errors consistently
   * @param error Axios error object
   * @returns Error object with appropriate message
   */
  private static handleError(error: AxiosError): Error {
    if (error.response) {
      const status = error.response.status;
      let errorMessage = `Request failed with status: ${status}`;

      try {
        const errorData = error.response.data as ApiErrorResponse;

        if (errorData.message) {
          errorMessage = errorData.message;
        } else if (errorData.errors) {
          const errorMessages = Object.entries(errorData.errors)
            .map(([field, messages]) => `${field}: ${messages.join(", ")}`)
            .join("; ");

          errorMessage = errorMessages || errorMessage;
        }
      } catch {}

      return new Error(errorMessage);
    }

    if (error.request) {
      return new Error("Network error: No response received from server");
    }

    return new Error(error.message || "An unexpected error occurred");
  }

  /**
   * Make a GET request
   * @param url URL to fetch (relative to base URL)
   * @param config Additional axios config
   * @returns Parsed response data
   */
  protected static async get<T>(
    url: string,
    config?: Parameters<AxiosInstance["get"]>[1],
  ): Promise<T> {
    const response = await this.getInstance().get<T>(url, config);
    return response.data;
  }

  /**
   * Make a POST request
   * @param url URL to post to (relative to base URL)
   * @param data Data to send
   * @param config Additional axios config
   * @returns Parsed response data
   */
  protected static async post<T>(
    url: string,
    data?: Parameters<AxiosInstance["post"]>[1],
    config?: Parameters<AxiosInstance["post"]>[2],
  ): Promise<T> {
    const response = await this.getInstance().post<T>(url, data, config);
    return response.data;
  }

  /**
   * Make a PUT request
   * @param url URL to put to (relative to base URL)
   * @param data Data to send
   * @param config Additional axios config
   * @returns Parsed response data
   */
  protected static async put<T>(
    url: string,
    data: Parameters<AxiosInstance["put"]>[1],
    config?: Parameters<AxiosInstance["put"]>[2],
  ): Promise<T> {
    const response = await this.getInstance().put<T>(url, data, config);
    return response.data;
  }

  /**
   * Make a DELETE request
   * @param url URL to delete (relative to base URL)
   * @param config Additional axios config
   * @returns Parsed response data or void
   */
  protected static async delete<T = void>(
    url: string,
    config?: Parameters<AxiosInstance["delete"]>[1],
  ): Promise<T> {
    const response = await this.getInstance().delete<T>(url, config);
    return response.data;
  }
}
