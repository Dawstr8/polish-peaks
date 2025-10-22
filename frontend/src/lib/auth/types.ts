export enum TokenTypes {
  ACCESS = "access",
  REFRESH = "refresh",
}

export interface Token {
  access_token: string;
  token_type: string;
}

export interface OAuth2PasswordRequest {
  username: string;
  password: string;
}
