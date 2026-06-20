/**
 * The cabinet is a thin client over the FastAPI backend. Rather than hit the API
 * cross-origin from the browser, we proxy `/api/*` to the backend server-side, so
 * the browser only ever talks to the cabinet's own origin (no CORS in the path).
 *
 * @type {import('next').NextConfig}
 */
const target = process.env.API_PROXY_TARGET || "http://127.0.0.1:8000";

const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    return [{ source: "/api/:path*", destination: `${target}/:path*` }];
  },
};

export default nextConfig;
