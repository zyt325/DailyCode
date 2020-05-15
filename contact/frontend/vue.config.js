const path = require("path");
// const target_host = "10.14.6.159:5000";
// const target_host = "127.0.0.1:5000";
const target_host = "docker03.base-fx.com:8085"

module.exports = {
    devServer: {
        host: "localhost",
        compress: true,
        proxy: {
            "/api": {
                target: "http://" + target_host + "/api",
                ws: true,
                changeOrigin: true,
                pathRewrite: {
                    "^/api": ""
                }
            }
        }
    },
    pages: {
        address_book: {
            //   // page 的入口
            entry: "src/address_book/main.js",
            //   // 模板来源
            //   template: 'public/index.html',
            //   // 在 dist/index.html 的输出
            filename: "index.html",
            //   // 当使用 title 选项时，
            //   // template 中的 title 标签需要是 <title><%= htmlWebpackPlugin.options.title %></title>
            title: "员工通讯录 Staff Directory",
            //   // 在这个页面中包含的块，默认情况下会包含
            //   // 提取出来的通用 chunk 和 vendor chunk。
            chunks: ["chunk-vendors", "chunk-common", "address_book"]
        }
        //     当使用只有入口的字符串格式时，
        //     模板会被推导为 `public/subpage.html`
        //     并且如果找不到的话，就回退到 `public/index.html`。
        // 输出文件名会被推导为`subpage.html`。
        // subpage: 'src/tools/main.js'
    },

    chainWebpack: (config) => {
        // 因为是多页面，所以取消 chunks，每个页面只对应一个单独的 JS / CSS
        config.optimization
            .splitChunks({
                cacheGroups: {}
            })
    },
    // 是否开启eslint保存检测，有效值：ture | false | 'error'
    lintOnSave: false,

    // 运行时版本是否需要编译
    runtimeCompiler: false,
    // 如果你不需要生产环境的 source map，可以将其设置为 false 以加速生产环境构建
    productionSourceMap: false,

    css: {
        // 默认生产环境下是 true，开发环境下是 false
        extract: true,
        // 是否为 CSS 开启 source map。设置为 true 之后可能会影响构建的性能
        sourceMap: false,
    }
};
