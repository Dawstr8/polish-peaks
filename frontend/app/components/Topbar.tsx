"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { Button } from "@/components/ui/button";
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet";
import { Menu } from "lucide-react";
import Logo from "./Logo";
import { navigation } from "@/app/config/navigation";

export default function Topbar() {
  const pathname = usePathname();

  return (
    <header className="bg-white shadow-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Logo />

          {/* Desktop Navigation */}
          <nav className="hidden md:flex space-x-2">
            {navigation.map((route) => {
              const isActive = pathname === route.href;

              return (
                <Button
                  key={route.name}
                  asChild
                  variant={isActive ? "default" : "ghost"}
                >
                  <Link href={route.href}>{route.name}</Link>
                </Button>
              );
            })}
          </nav>

          {/* Desktop CTA */}
          <div className="hidden md:flex items-center">
            {/* Upload Button */}
            <Button asChild>
              <Link href="/upload">Share Your Summit</Link>
            </Button>
          </div>

          {/* Mobile menu */}
          <Sheet>
            <SheetTrigger asChild>
              <Button variant="ghost" size="icon" className="md:hidden">
                <Menu className="h-6 w-6" />
                <span className="sr-only">Toggle menu</span>
              </Button>
            </SheetTrigger>
            <SheetContent side="right" className="w-[300px]">
              <div className="flex flex-col space-y-4 mt-8">
                {navigation.map((route) => {
                  const isActive = pathname === route.href;
                  return (
                    <Button
                      key={route.name}
                      asChild
                      variant={isActive ? "default" : "ghost"}
                    >
                      <Link href={route.href}>{route.name}</Link>
                    </Button>
                  );
                })}

                {/* Mobile Upload Button */}
                <Button asChild className="mt-4">
                  <Link href="/upload">Share Your Summit</Link>
                </Button>
              </div>
            </SheetContent>
          </Sheet>
        </div>
      </div>
    </header>
  );
}
