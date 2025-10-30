"use client";

import LogoutButton from "./LogoutButton";
import { User } from "@/lib/users/types";
import Link from "next/link";
import { Button } from "@/components/ui/button";

interface ActionsProps {
  user: User | null;
  className?: string;
}

export default function Actions({ user, className }: ActionsProps) {
  return (
    <div className={className}>
      {user ? (
        <>
          <span className="text-sm text-muted-foreground">{user.email}</span>
          <LogoutButton />
        </>
      ) : (
        <Button asChild variant="outline">
          <Link href="/login">Sign In</Link>
        </Button>
      )}

      <Button asChild>
        <Link href="/upload">Share Your Summit</Link>
      </Button>
    </div>
  );
}
