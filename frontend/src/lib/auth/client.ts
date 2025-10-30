import { API_ENDPOINTS } from "@/config/api";
import { ApiClient } from "@/lib/common/api-client";
import { User, UserCreate } from "@/lib/users/types";

/**
 * AuthClient class for handling user-related API requests
 */
export class AuthClient extends ApiClient {
  static async login(email: string, password: string): Promise<User> {
    const formData = new FormData();
    formData.append("email", email);
    formData.append("password", password);

    await this.post(API_ENDPOINTS.auth.login, formData);
    return this.me();
  }

  static async register(userCreate: UserCreate): Promise<User> {
    return this.post<User>(API_ENDPOINTS.auth.register, userCreate);
  }

  static async me(): Promise<User> {
    return this.get<User>(API_ENDPOINTS.auth.me);
  }

  static async logout(): Promise<void> {
    return this.post(API_ENDPOINTS.auth.logout);
  }
}
