const path = require('path');

module.exports = {
    publicPath: process.env.NODE_ENV === 'production'
      ? '/LUCY-test/'  // 替換為您的倉庫名
      : '/',
    outputDir: path.resolve(__dirname, '../docs'),  // 輸出到根目錄的 docs
}