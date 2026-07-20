import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Spoon — Document Intelligence",
  description: "Upload any PDF and ask questions. Powered by local AI with RAG.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
