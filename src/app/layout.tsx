import { PolicyEngineShell } from "@policyengine/ui-kit/layout";
import "@policyengine/ui-kit/styles.css";

import type { Metadata, Viewport } from 'next';
import Script from 'next/script';
import './globals.css';

// The canonical address: policyengine.org serves this app through a zone
// rewrite, so links and link previews name it, not the Vercel deployment.
const SITE_URL = 'https://policyengine.org/us/child-tax-credit-2024-election-calculator';
const TITLE = 'Vance and Harris CTC comparison | PolicyEngine';
const DESCRIPTION =
  'Calculate and compare the impact of the Vance and Harris Child Tax Credit proposals on your household, powered by PolicyEngine US microsimulation.';

export const metadata: Metadata = {
  // metadataBase carries the base path. Next.js joins its path onto relative
  // metadata URLs, and file-based images such as opengraph-image already
  // include the base path, so one added here would 404 with the path doubled.
  // Use absolute URLs for any image added later.
  metadataBase: new URL(SITE_URL),
  title: TITLE,
  description: DESCRIPTION,
  authors: [{ name: 'PolicyEngine' }],
  alternates: { canonical: SITE_URL },
  openGraph: {
    type: 'website',
    url: SITE_URL,
    title: TITLE,
    description: DESCRIPTION,
    siteName: 'PolicyEngine',
  },
  twitter: {
    card: 'summary_large_image',
    title: TITLE,
    description: DESCRIPTION,
    site: '@ThePolicyEngine',
  },
};

export const viewport: Viewport = {
  width: 'device-width',
  initialScale: 1,
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link
          rel="preconnect"
          href="https://fonts.gstatic.com"
          crossOrigin="anonymous"
        />
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap"
          rel="stylesheet"
        />
      </head>
      <body>
        <PolicyEngineShell country="us">{children}        </PolicyEngineShell>
        {/* Google Analytics: policyengine.org's GA4 property; this app is served at
            policyengine.org/us/child-tax-credit-2024-election-calculator through a rewrite, where the main site's GA does not reach. */}
        {process.env.NODE_ENV === 'production' && (
          <>
            <Script
              src="https://www.googletagmanager.com/gtag/js?id=G-2YHG89FY0N"
              strategy="afterInteractive"
            />
            <Script id="google-analytics" strategy="afterInteractive">
              {`window.dataLayer = window.dataLayer || [];
function gtag(){dataLayer.push(arguments);}
gtag('js', new Date());
gtag('config', 'G-2YHG89FY0N');`}
            </Script>
          </>
        )}
      </body>
    </html>
  );
}
