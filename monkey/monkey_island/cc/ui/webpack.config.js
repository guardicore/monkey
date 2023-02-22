const path = require('path');

var isProduction = process.argv[process.argv.indexOf('--mode') + 1] === 'production';

const SpeedMeasurePlugin = require('speed-measure-webpack-plugin');
const HtmlWebPackPlugin = require('html-webpack-plugin');
const NodePolyfillPlugin = require('node-polyfill-webpack-plugin');
const ForkTsCheckerWebpackPlugin = require('fork-ts-checker-webpack-plugin');
const smp = new SpeedMeasurePlugin({disable: isProduction});


module.exports = smp.wrap({
  mode: isProduction ? 'production' : 'development',
  module: {
    noParse: /iconv-loader\.js/,
    rules: [
      {
        test: /\.tsx?$/,
        use: ['thread-loader', {
          loader: 'ts-loader',
          options: {
            transpileOnly: true,
            happyPackMode: true
          }
        }]
      },
      {
        test: /\.js$/,
        use: ['thread-loader', 'source-map-loader'],
        enforce: 'pre'
      },
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: ['thread-loader', {
          loader: 'babel-loader',
          options: {
            cacheDirectory: true
          }
        }]
      },
      {
        test: /\.css$/,
        use: [
          'thread-loader',
          'style-loader',
          'css-loader'
        ]
      },
      {
        test: /\.scss$/,
        use: [
          'thread-loader',
          'style-loader',
          'css-loader',
          'sass-loader'
        ]
      },
      {
        test: /\.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/,
        type: 'asset/resource'
      },
      {
        test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
        type: 'asset'
      },
      {
        test: /\.(png|jpg|gif)$/,
        type: 'asset'
      },
      {
        test: /\.html$/,
        use: [
          {
            loader: 'html-loader'
          }
        ]
      }
    ]
  },
  ignoreWarnings: [/Failed to parse source map/],
  devtool: isProduction ? 'source-map' : 'eval-source-map',
  plugins: [
    new ForkTsCheckerWebpackPlugin({
      typescript: {
        diagnosticOptions: {
          semantic: true,
          syntactic: true
        }
      }
    }),
    new HtmlWebPackPlugin({
      template: './src/index.html',
      filename: './index.html'
    }),
    new NodePolyfillPlugin()
  ],
  resolve: {
    extensions: ['.ts', '.tsx', '.js', '.jsx', '.css'],
    modules: [
      'node_modules',
      path.resolve(__dirname, 'src/')
    ],
    fallback: {
      //"buffer": require.resolve("buffer/"),
      //"http": require.resolve("stream-http"),
      //"url": require.resolve("url/"),
      //"util": require.resolve("util/"),
      //"stream": require.resolve("stream-browserify"),
      //"zlib": require.resolve("browserify-zlib"),
      //"https": require.resolve("https-browserify")
      //"buffer": false,
      //"http": false,
      //"url": false,
      //"util": false,
      //"stream": false,
      //"zlib": false,
      //"https": false,
      //"path": false
      "fs": false
    }
  },
  output: {
    publicPath: '/'
  },
  devServer: {
    host: '0.0.0.0',
    proxy: {
      '/api': {
        target: 'https://localhost:5000',
        secure: false,
        changeOrigin: true
      }
    }
  }
});
