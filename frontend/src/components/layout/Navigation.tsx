"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { navigation } from "@/config/navigation";
import {
  NavigationMenu,
  NavigationMenuItem,
  NavigationMenuLink,
  NavigationMenuList,
  navigationMenuTriggerStyle,
} from "@/components/ui/navigation-menu";

export interface NavigationProps {
  className?: string;
  listClassName?: string;
  orientation?: "horizontal" | "vertical";
}

export default function Navigation({
  className,
  listClassName,
  orientation = "horizontal",
}: NavigationProps) {
  const pathname = usePathname();

  return (
    <NavigationMenu className={className} orientation={orientation}>
      <NavigationMenuList className={listClassName}>
        {navigation.map((route) => {
          const isActive = pathname === route.href;
          return (
            <NavigationMenuItem key={route.name}>
              <NavigationMenuLink asChild>
                <Link
                  href={route.href}
                  className={navigationMenuTriggerStyle()}
                  data-active={isActive}
                >
                  {route.name}
                </Link>
              </NavigationMenuLink>
            </NavigationMenuItem>
          );
        })}
      </NavigationMenuList>
    </NavigationMenu>
  );
}
