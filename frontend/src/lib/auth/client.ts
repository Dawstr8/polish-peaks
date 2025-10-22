import { API_ENDPOINTS } from "@/config/api";
import { ApiClient } from "@/lib/common/api-client";
import { Token, OAuth2PasswordRequest } from "@/lib/auth/types";
import { User, UserCreate } from "@/lib/users/types";

/**
 * AuthClient class for handling user-related API requests
 */
export class AuthClient extends ApiClient {
  static async login(loginForm: OAuth2PasswordRequest): Promise<Token> {
    const formData = new FormData();
    formData.append("username", loginForm.username);
    formData.append("password", loginForm.password);

    return this.post<Token>(API_ENDPOINTS.auth.login, formData);
  }

  static async register(userCreate: UserCreate): Promise<User> {
    return this.post<User>(API_ENDPOINTS.auth.register, userCreate);
  }
}
