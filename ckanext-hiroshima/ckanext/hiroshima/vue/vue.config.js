const PrettierPlugin = require('prettier-webpack-plugin')

module.exports = {
  "publicPath": "./",
  "outputDir": "../public/dist",
  "transpileDependencies": [
    "vuetify"
  ],
  configureWebpack: {
    plugins: [
      new PrettierPlugin({
        singleQuote: true,
        semi: false,
        tabWidth: 2
      })
    ]
  },
  chainWebpack: config => {
    //チャンクファイルを生成しないようにする
    config.optimization.delete('splitChunks')
  }
}
