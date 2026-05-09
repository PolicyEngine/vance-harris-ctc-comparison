import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  // Mantine ships CJS interop and relies on browser globals.
  // Transpile so Next can render its components without ESM/CJS mismatch.
  transpilePackages: ['@mantine/core', '@mantine/hooks'],
  // Pin the workspace root so Turbopack does not silently pick up a stray
  // lockfile from a parent directory during local development or CI.
  turbopack: {
    root: process.cwd(),
  },
};

export default nextConfig;
