<template>
  <el-container id="add">
    <el-header>
      <div class="article_title">
        <el-input v-model="articleTitle" placeholder="请输入标题" class="input-with-select">
          <el-cascader
            style="width:120px"
            :props="defaultParams"
            :options="cascader_data"
            v-model="articleCategory"
            :clearable="true"
            slot="prepend"
          ></el-cascader>
        </el-input>
      </div>
      <div class="article_submit">
        <el-input style="width:180px" v-model="articlePwd" type="password" placeholder="请输入密码">
          <el-button slot="append" :plain="true" @click="submitArticle()">提交</el-button>
        </el-input>
      </div>
    </el-header>
    <el-container>
      <el-main>
        <template>
          <div :id="editor_area"></div>
        </template>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
    import "element-ui/lib/theme-chalk/index.css";
    import $ from "jquery";
    import uuid from "uuid/v4";
    import {token} from "../commonFunction/token"
    import {editor} from "../commonFunction/editor"

    export default {
        name: "MarkdownEditor",
        data() {
            return {
                articleTitle: "",
                title_warn: "",
                articlePwd: "",
                cascader_data: [],
                articleCategory: [],
                defaultParams: {
                    checkStrictly: true,
                    label: "name",
                    value: "id",
                    children: "sub_cat",
                    emitPath: false
                },
                //最终生成的编辑器
                editor: null,
                //默认选项
                defaultOptions: {
                    width: "100%",
                    height: "calc(100% - 60px)",
                    path: "/editor.md/lib/",
                    placeholder: "本编辑器支持Markdown编辑，左边编写，右边预览",
                    imageUpload: true,
                    imageFormats: ["jpg", "jpeg", "gif", "png", "bmp", "webp"],
                    imageUploadURL: "/dj_note/upload/",
                    saveHTMLToTextarea: true,
                    emoji: false,
                    taskList: true,
                    tocm: true, // Using [TOCM]
                    toolbarIcons: function () {
                        //自定义工具栏，后面有详细介绍
                        return editormd.toolbarModes["full"]; // full, simple, mini
                        // Using "||" set icons align right.
                        // return ["undo", "redo", "|", "bold", "hr", "|", "preview", "watch", "|", "fullscreen", "info", "testIcon", "testIcon2", "file", "faicon", "||", "watch", "fullscreen", "preview", "testIcon"]
                    }
                }
            };
        },
        props: {
            /**
             * editormd挂载元素的id
             */
            editor_area: {
                type: String,
                default: uuid()
            },
            /**
             * editormd的选项对象
             */
            options: {
                type: Object
            }
        },
        mounted() {
            let vm = this;
            //加载editormd
            this.requireEditor(function () {
                vm.editor = editormd(vm.editor_area, vm.getOptions());
            });

            if (!this.get_session_key("tools_token")) {
                this.get_token();
                this.get_categorys();
            } else {
                this.get_categorys();
            }
        },
        mixins: [token, editor],
        methods: {
            requireEditor(callback) {
                let vm = this;
                //设置全局变量，因为editormd依赖jquery
                window.$ = window.jQuery = $;
                //异步加载并执行
                $.getScript("/editor.md/editormd.min.js", function (script) {
                    callback();
                });
                //加载css
                $("head").append(
                    $('<link rel="stylesheet" type="text/css" />').attr(
                        "href",
                        "/editor.md/css/editormd.min.css"
                    )
                );
            },
            /**
             * 得到最终的options，组件属性上获得的选项覆盖此处的默认选项
             */
            getOptions() {
                return Object.assign(this.defaultOptions, this.options);
            },
            submitArticle1() {
                console.log(
                    this.articleCategory,
                    this.articleTitle,
                    this.articlePwd,
                    this.editor.getMarkdown()
                );
            },
            titleWarn() {
                this.$message.warning(this.title_warn);
            },
            submitArticle() {
                // 标题不能为空
                var _this = this;
                if (this.articleTitle == "") {
                    this.title_warn = "标题不能为空";
                    this.titleWarn();
                } else if (this.articleCategory == "") {
                    this.title_warn = "请选择类别";
                    this.titleWarn();
                } else {
                    this.axios
                        .post(
                            "/dj_note/add/",
                            "class_id=" +
                            encodeURIComponent(this.articleCategory) +
                            "&title=" +
                            encodeURIComponent(this.articleTitle) +
                            "&secret=" +
                            encodeURIComponent(this.articlePwd) +
                            "&body=" +
                            encodeURIComponent(this.editor.getMarkdown()) +
                            "&body_html=" +
                            encodeURIComponent(this.editor.getPreviewedHTML())
                        )
                        .then(function (response) {
                            if (
                                Object.prototype.toString.call(response.data) ===
                                "[object Object]" &&
                                response.data["status"] == 1
                            ) {
                                _this.title_warn = "提交成功";
                                _this.titleWarn();
                                window.location.href =
                                    "/media/articles/" + response.data["result"]["filename"];
                            } else if (response.data == 2) {
                                _this.title_warn = "标题已经存在";
                                _this.titleWarn();
                            } else if (response.data == 3) {
                                _this.title_warn = "操作密码错误";
                                _this.titleWarn();
                            } else if (response.data == 4) {
                                _this.title_warn = "保存失败";
                                _this.titleWarn();
                            }
                        });
                }
            }
        }
    };
</script>

<style>
  @import url("/editor.md/examples/css/style.css");

  * {
    margin: 0;
    padding: 0;
  }

  html,
  body {
    height: 100%;
  }

  #app {
    height: 100%;
  }

  #app > .el-container {
    height: 100%;
  }

  .el-header {
    background-color: #b3c0d1;
    color: #333;
    line-height: 60px;
  }

  .article_title {
    float: left;
    text-align: center;
    line-height: 60px;
  }

  .article_title .el-input-group__prepend {
    padding: 0px !important;
  }

  .article_submit {
    float: right;
    margin-right: 5px;
    line-height: 60px;
  }

  .input-with-select .el-input-group__prepend {
    background-color: #fff;
  }

  .el-aside {
    width: 200px !important;
    height: 100%;
    background-color: #d3dce6;
    color: #333;
    text-align: left;
  }
</style>
