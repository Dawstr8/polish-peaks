import Link from "next/link";
import { Button } from "@/src/components/ui/button";
import { Mountain, Github, Mail } from "lucide-react";
import Logo from "./Logo";
import { navigation } from "@/src/config/navigation";

export default function Footer() {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="border-t bg-muted">
      <div className="mx-auto max-w-7xl px-6 py-12 lg:px-8">
        {/* Main footer content */}
        <div className="xl:grid xl:grid-cols-3 xl:gap-8">
          {/* Company section */}
          <div className="space-y-6">
            <Logo />
            <p className="text-sm leading-6 text-muted-foreground">
              Document and share your mountain adventures across Poland. Track
              peaks, weather conditions, and create lasting memories of your
              summit conquests.
            </p>
            <div className="flex space-x-2">
              <Button variant="ghost" size="sm" asChild>
                <Link
                  href="https://github.com/Dawstr8/polish-peaks"
                  aria-label="GitHub"
                >
                  <Github className="h-4 w-4" />
                </Link>
              </Button>
              <Button variant="ghost" size="sm" asChild>
                <Link href="mailto:dawid.strojek@gmail.com" aria-label="Email">
                  <Mail className="h-4 w-4" />
                </Link>
              </Button>
            </div>
          </div>

          {/* Navigation Links */}
          <div className="mt-16 xl:col-span-2 xl:mt-0">
            <h3 className="text-sm font-semibold leading-6 text-foreground">
              Navigation
            </h3>
            <ul
              role="list"
              className="mt-6 grid grid-cols-2 gap-4 sm:grid-cols-4"
            >
              {navigation.map((route) => (
                <li key={route.name}>
                  <Button variant="link" className="p-0" asChild>
                    <Link href={route.href}>{route.name}</Link>
                  </Button>
                </li>
              ))}
            </ul>
          </div>
        </div>

        {/* Bottom border */}
        <div className="mt-16 border-t pt-8 sm:mt-20 lg:mt-24">
          <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between">
            <div className="flex items-center space-x-2 text-sm text-muted-foreground">
              <Mountain className="h-4 w-4" />
              <span>Made with passion for Polish mountains</span>
            </div>
            <p className="mt-4 text-sm text-muted-foreground sm:mt-0">
              &copy; {currentYear} Polish Peaks. All rights reserved.
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
}
