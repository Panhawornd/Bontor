import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Bontor - AI-Powered Major and Career Guidance for Cambodian BacII Students",
  description: "AI-powered Major, University, and Career Recommendations System for Cambodian BacII Students",
  icons: {
    icon: '/icon-with-bg.svg',
    shortcut: '/icon-with-bg.svg',
    apple: '/icon-with-bg.svg',
  },
  openGraph: {
    title: "Bontor - AI-Powered Major and Career Guidance for Cambodian BacII Students",
    description: "AI-powered Major, University, and Career Recommendations System for Cambodian BacII Students",
      images: [
      {
        url: '/icon-with-bg.svg',
        width: 1200,
        height: 630,
        alt: 'Bontor Logo',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: "Bontor - AI-Powered Major and Career Guidance for Cambodian BacII Students",
    description: "AI-powered Major, University, and Career Recommendations System for Cambodian BacII Students",
    images: ['/icon-with-bg.svg'],
  },
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
        {children}
      </body>
    </html>
  );
}
