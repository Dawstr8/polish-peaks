"use client";

import { useAuth } from "@/components/auth/AuthContext";
import Logo from "./Logo";
import HamburgerMenu from "./HamburgerMenu";
import Navigation from "./Navigation";
import Profile from "./Profile";
import CallToAction from "./CallToAction";

export default function Topbar() {
  const { user } = useAuth();

  return (
    <header className="bg-white shadow-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          <Logo />
          <Navigation className="hidden md:flex" listClassName="space-x-2" />
          <div className="hidden md:flex space-x-2 items-center justify-center">
            <Profile user={user} />
            <CallToAction />
          </div>
          <div className="md:hidden">
            <HamburgerMenu>
              <div className="flex flex-col space-y-4 mt-8">
                <Navigation
                  listClassName="flex flex-col space-y-2 mx-4"
                  orientation="vertical"
                />
                <div className="flex flex-col space-y-2 mx-4">
                  <CallToAction />
                  <Profile user={user} />
                </div>
              </div>
            </HamburgerMenu>
          </div>
        </div>
      </div>
    </header>
  );
}
