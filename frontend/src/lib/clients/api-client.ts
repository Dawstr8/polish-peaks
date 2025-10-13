/**
 * Base API client class for making HTTP requests to the backend
 */

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
  /**
   * Handles API errors consistently
   * @param response Fetch Response object
   * @returns Error object with appropriate message
   */
  protected static async handleError(response: Response): Promise<Error> {
    let errorMessage = `Request failed with status: ${response.status}`;

    try {
      const errorData = (await response.json()) as ApiErrorResponse;

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

  /**
   * Make a GET request
   * @param url URL to fetch
   * @param options Fetch options
   * @returns Parsed response
   */
  protected static async get<T>(
    url: string,
    options?: RequestInit,
  ): Promise<T> {
    const response = await fetch(url, {
      method: "GET",
      headers: {
        Accept: "application/json",
        ...options?.headers,
      },
      ...options,
    });

    if (!response.ok) {
      throw await this.handleError(response);
    }

    return response.json();
  }

  /**
   * Make a POST request
   * @param url URL to post to
   * @param data Data to send
   * @param options Fetch options
   * @returns Parsed response
   */
  protected static async post<T>(
    url: string,
    data?: unknown,
    options?: RequestInit,
  ): Promise<T> {
    const isFormData = data instanceof FormData;

    const response = await fetch(url, {
      method: "POST",
      headers: {
        ...(!isFormData ? { "Content-Type": "application/json" } : {}),
        Accept: "application/json",
        ...options?.headers,
      },
      body: isFormData ? data : JSON.stringify(data),
      ...options,
    });

    if (!response.ok) {
      throw await this.handleError(response);
    }

    return response.json();
  }

  /**
   * Make a PUT request
   * @param url URL to put to
   * @param data Data to send
   * @param options Fetch options
   * @returns Parsed response
   */
  protected static async put<T>(
    url: string,
    data: unknown,
    options?: RequestInit,
  ): Promise<T> {
    const isFormData = data instanceof FormData;

    const response = await fetch(url, {
      method: "PUT",
      headers: {
        ...(!isFormData ? { "Content-Type": "application/json" } : {}),
        Accept: "application/json",
        ...options?.headers,
      },
      body: isFormData ? data : JSON.stringify(data),
      ...options,
    });

    if (!response.ok) {
      throw await this.handleError(response);
    }

    return response.json();
  }

  /**
   * Make a DELETE request
   * @param url URL to delete
   * @param options Fetch options
   * @returns Parsed response or void
   */
  protected static async delete<T = void>(
    url: string,
    options?: RequestInit,
  ): Promise<T> {
    const response = await fetch(url, {
      method: "DELETE",
      headers: {
        Accept: "application/json",
        ...options?.headers,
      },
      ...options,
    });

    if (!response.ok) {
      throw await this.handleError(response);
    }

    if (response.status === 204) {
      return {} as T;
    }

    return response.json();
  }
}
