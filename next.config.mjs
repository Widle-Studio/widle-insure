/** @type {import('next').NextConfig} */
const nextConfig = {
    // If not routing to custom domains via Vercel directly but instead proxying locally:
    // rewrites: async () => {
    //     return [
    //         {
    //             source: '/api/:path*',
    //             destination:
    //                 process.env.NODE_ENV === 'development'
    //                     ? 'http://127.0.0.1:8000/api/:path*'
    //                     : '/api/:path*',
    //         },
    //     ]
    // },
}

export default nextConfig
