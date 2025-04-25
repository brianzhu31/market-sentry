import type { Metadata } from "next";
import { ReactNode } from "react";
import { Inter } from "next/font/google";
import { Toaster } from "@/components/ui/toaster";
import { CompaniesProvider } from "@/context/companies-context";
import { UserSessionProvider } from "@/context/user-session-context";
import "./globals.css";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "Market Sentry",
  description: "",
};

interface RootLayoutProps {
  children: ReactNode;
}

export default async function RootLayout({
  children,
}: RootLayoutProps) {
  return (
    <UserSessionProvider>
      <CompaniesProvider>
        <RootLayoutContent>{children}</RootLayoutContent>
      </CompaniesProvider>
    </UserSessionProvider>
  );
}

export function RootLayoutContent({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={inter.className}>
        <main>{children}</main>
        <Toaster />
      </body>
    </html>
  );
}
