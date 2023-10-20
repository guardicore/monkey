/** @type {import('next').NextConfig} */
const nextConfig = {
    reactStrictMode: true,
    env: {},
    typescript: {
        // !! WARN !!
        // Dangerously allow production builds to successfully complete even if
        // your project has type errors.
        // !! WARN !!
        ignoreBuildErrors: true,
    },
};

//eslint-disable-next-line no-undef
module.exports = nextConfig;
