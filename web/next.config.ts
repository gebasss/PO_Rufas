import type { NextConfig } from 'next'

// Exportação estática: o build gera HTML/JS/CSS em `out/`, servido pelo servidor Python do projeto.
// Em desenvolvimento (`next dev`), as chamadas /api/* são encaminhadas ao servidor Python na porta 8000.
const nextConfig: NextConfig = {
  output: 'export',
  trailingSlash: true,
  images: { unoptimized: true },
  reactStrictMode: true,
  ...(process.env.NODE_ENV === 'development'
    ? { rewrites: async () => [{ source: '/api/:path*', destination: 'http://127.0.0.1:8000/api/:path*' }] }
    : {})
}

export default nextConfig
