import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "NomosAI",
  description: "Legal AI Assistant",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
