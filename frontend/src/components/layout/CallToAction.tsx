import { Button } from "@/components/ui/button";
import Link from "next/link";
import { Camera } from "lucide-react";

export default function CallToAction() {
  return (
    <Button asChild>
      <Link href="/upload">
        <Camera className="h-4 w-4" />
        Share Your Summit
      </Link>
    </Button>
  );
}
