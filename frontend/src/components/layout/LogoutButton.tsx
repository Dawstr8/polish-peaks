"use client";

import { useAuth } from "@/components/auth/AuthContext";
import { AuthClient } from "@/lib/auth/client";
import { cn } from "@/lib/utils";
import { LogOut } from "lucide-react";

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
    <button
      className={cn("flex gap-2 items-center justify-center", className)}
      onClick={handleSignOut}
    >
      <LogOut className="h-4 w-4" />
      Sign Out
    </button>
  );
}
