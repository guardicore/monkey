/** @type {import('next').NextConfig} */
const keepConsoleErrors =
    //eslint-disable-next-line no-undef
    process.env.NODE_ENV === process.env.NEXT_PUBLIC_PRODUCTION_KEY
        ? {
              exclude: ['error']
          }
        : false;

const nextConfig = {
    reactStrictMode: true,
    compiler: {
        removeConsole: keepConsoleErrors
    },
    output: 'standalone'
};

//eslint-disable-next-line no-undef
module.exports = nextConfig;
