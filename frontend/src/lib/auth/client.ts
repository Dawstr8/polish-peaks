import { API_ENDPOINTS } from "@/config/api";
import { ApiClient } from "@/lib/common/api-client";
import { User, UserCreate } from "@/lib/users/types";

/**
 * AuthClient class for handling user-related API requests
 */
export class AuthClient extends ApiClient {
  static async login(email: string, password: string): Promise<void> {
    const formData = new FormData();
    formData.append("email", email);
    formData.append("password", password);

    return this.post(API_ENDPOINTS.auth.login, formData);
  }

  static async register(userCreate: UserCreate): Promise<User> {
    return this.post<User>(API_ENDPOINTS.auth.register, userCreate);
  }
}
