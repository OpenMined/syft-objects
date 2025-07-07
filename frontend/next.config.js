/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  distDir: 'out',
  images: {
    unoptimized: true,
  },
  // Since we're serving from /widget/ path
  basePath: process.env.NODE_ENV === 'production' ? '/widget' : '',
  assetPrefix: process.env.NODE_ENV === 'production' ? '/widget' : '',
  trailingSlash: true,
}

module.exports = nextConfig
