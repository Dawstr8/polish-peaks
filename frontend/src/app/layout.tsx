import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "../styles/globals.css";
import Topbar from "@/components/layout/Topbar";
import Footer from "@/components/layout/Footer";
import { QueryProvider } from "./query-provider";
import { Toaster } from "@/components/ui/sonner";
import { AuthProvider } from "@/components/auth/AuthContext";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Polish Peaks - Document Your Mountain Adventures",
  description:
    "Track and share your conquests of Polish mountain peaks with weather data, locations, and beautiful memories. A social platform for mountain enthusiasts.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <AuthProvider>
          <div className="flex min-h-screen flex-col">
            <Topbar />
            <QueryProvider>
              <main className="flex-1">{children}</main>
            </QueryProvider>
            <Footer />
            <Toaster position="top-center" />
          </div>
        </AuthProvider>
      </body>
    </html>
  );
}
