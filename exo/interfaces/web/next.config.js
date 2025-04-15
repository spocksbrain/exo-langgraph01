/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*', // Proxy to backend
      },
      {
        source: '/ws',
        destination: 'http://localhost:8000/ws', // Proxy to WebSocket
      },
    ]
  },
}

module.exports = nextConfig
