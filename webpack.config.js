var webpack = require("webpack")
var path = require("path")

var BUILD_DIR = path.resolve(__dirname, "public")
var APP_DIR = path.resolve(__dirname, "src")

var config = {
  entry: APP_DIR + "/index.jsx",
  output: {
    path: BUILD_DIR,
    publicPath: "/public/",
    filename: "bundle.js"
  },
  module: {
    loaders: [
      {
        test: /\.jsx?/,
        include: APP_DIR,
        loader: "babel-loader"
      }
    ]
  },
  devtool: "source-map",
  devServer: {
    contentBase: __dirname,
    hot: true,
    filename: "bundle.js"
  },
  plugins: [
    new webpack.HotModuleReplacementPlugin()
  ]
}

module.exports = config
