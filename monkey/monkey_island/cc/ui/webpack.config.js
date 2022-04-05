const path = require('path');
const HtmlWebPackPlugin = require("html-webpack-plugin");

module.exports = {
  module: {
    rules: [
      { test: /\.tsx?$/,
        loader: "ts-loader"
      },
      {
        test: /\.js$/,
        loader: "source-map-loader"
      },
      {
        test: /\.js$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
        }
      },
      {
        test: /\.css$/,
        use: [
          'style-loader',
          'css-loader'
        ]
      },
      {
        test: /\.scss$/,
        use: [
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
            loader: "html-loader"
          }
        ]
      }
    ]
  },
  devtool: "source-map",
  plugins: [
    new HtmlWebPackPlugin({
      template: "./src/index.html",
      filename: "./index.html"
    })
  ],
  resolve: {
    extensions: ['.ts', '.tsx', '.js', '.jsx', '.css'],
    modules: [
      'node_modules',
      path.resolve(__dirname, 'src/')
    ]
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
};
