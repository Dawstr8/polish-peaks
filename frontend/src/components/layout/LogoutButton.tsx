"use client";

import { Button } from "@/components/ui/button";
import { useAuth } from "@/components/auth/AuthContext";
import { AuthClient } from "@/lib/auth/client";

export interface LogoutButtonProps {
  className?: string;
}

export default function LogoutButton({ className }: LogoutButtonProps) {
  const { logout } = useAuth();

  const handleSignOut = async () => {
    await AuthClient.logout();
    logout();
  };

  return (
    <Button className={className} variant="outline" onClick={handleSignOut}>
      Sign Out
    </Button>
  );
}
