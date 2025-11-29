// /** @type {import('next').NextConfig} */
// const nextConfig = {
//   async rewrites() {
//     return [
//       {
//         source: '/api/:path*',
//         destination: 'http://127.0.0.1:5000/api/:path*', // Redireciona para o Flask (Python)
//       },
//     ]
//   },
// }

// export default nextConfig




/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        // Usa a variável BACKEND_URL se existir (na nuvem), senão usa localhost (no seu PC)
        destination: (process.env.BACKEND_URL || 'http://127.0.0.1:5000') + '/api/:path*',
      },
    ]
  },
}

export default nextConfig;