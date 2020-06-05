<template>
  <el-container>
    <el-header>
      <div class="logo">
        <!--        <a>Note</a>-->
        <el-button icon="el-icon-s-fold" @click="toggleCollapsed"></el-button>
      </div>
      <div class="search">
        <el-input
          placeholder="请输入内容"
          v-model="search_word"
          @keyup.enter.native="get_article"
          class="input-with-select"
        >
        </el-input>
        <el-button icon="el-icon-search" @click="get_article()"></el-button>
        <el-button icon="el-icon-delete" @click="clear_search()"></el-button>
        <router-link target="_blank" :to="{path:'add/'}">
          <el-button icon="el-icon-document-add"></el-button>
        </router-link>
      </div>
    </el-header>

    <el-container>
      <el-aside :style="{width:aside.width+ 'px !important'}">
        <div>
          <el-menu
            class=" el-menu-vertical-demo"
            :unique-opened="true"
            @select="handleSelect"
            @open="handleSelect"
            @close="handleSelect"
            :collapse="isCollapse"
          >
            <template v-for="cat in category_list">
              <el-submenu
                :key="cat.id"
                :index="cat.id+''"
                :indexPath="cat.id"
                v-if="cat.type == 1 && cat.parent_category == null && cat.sub_cat.length"
              >
                <span slot="title">{{cat.name}}</span>
                <el-menu-item
                  v-for="sub_cat in cat.sub_cat"
                  :key="sub_cat.id"
                  :index="sub_cat.id+''"
                  :indexPath="sub_cat.id"
                >{{sub_cat.name}}
                </el-menu-item>
              </el-submenu>
              <el-menu-item
                :key="cat.id"
                :index="cat.id+''"
                :indexPath="cat.id"
                v-if="cat.type == 1 && cat.parent_category == null && !cat.sub_cat.length"
              >
                <span slot="title">{{cat.name}}</span>
              </el-menu-item>
            </template>
          </el-menu>
        </div>
      </el-aside>
      <el-main>
        <div>
          <el-table style="width: 99.9%" :show-header="false" :data="article_list">
            <el-table-column prop="title" label="#">
              <template slot-scope="article">
                <a
                  :href="'/media/articles/'+article.row.file_name"
                  target="_blank"
                  class="buttonText"
                >{{article.row.title}}</a>
              </template>
              <!-- 内部链接 -->
              <!-- <template slot-scope="article">
                <router-link
                  v-bind:to="'/media/articles/'+article.row.file_name"
                >{{article.row.title}}</router-link>
              </template>-->
            </el-table-column>
            <el-table-column fixed="right" label width="100">
              <template slot-scope="article">
                <router-link :to="'edit/?id='+article.row.id" target="_blank" class="buttonText">编辑</router-link>
              </template>
            </el-table-column>
          </el-table>
          <el-pagination
            @size-change="handleSizeChange"
            @current-change="handleCurrentChange"
            :current-page="page.cur_page"
            :page-sizes="[10, 15,20, 50]"
            :page-size="page.size"
            layout="total,sizes, prev, pager, next"
            :total="page.total"
            v-model="page"
          ></el-pagination>
        </div>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
    import "element-ui/lib/theme-chalk/index.css";
    import {token} from "../commonFunction/token"

    export default {
        data() {
            return {
                category_list: [],
                article_list: [],
                search_word: "",
                isCollapse: false,
                aside: {width: 300},
                page: {
                    total: 0,
                    category: 0,
                    size: 15,
                    offset: 0,
                    cur_page: 1
                }
            };
        },
        mounted() {
            if (this.get_session_key("tools_token")) {
                this.get_category();
                this.get_article();
            }
        },
        mixins: [token],
        methods: {
            toggleCollapsed() {
                this.isCollapse = !this.isCollapse;
                if (this.isCollapse) {
                    this.aside.width = 0;
                } else {
                    this.aside.width = 300;
                }
            },
            clear_search() {
                this.search_word = '';
                this.get_article();
            },
            get_category() {
                var _this = this;
                this.axios
                    .get("/api/v1/note_categorys?format=json", {
                        headers: {
                            Authorization: "JWT ".concat(this.get_session_key("tools_token"))
                        }
                    })
                    .then(function (res) {
                        _this.category_list = res.data;
                        // console.log(_this.category_list);
                    })
                    .catch(function (err) {
                        _this.get_category()
                    })
            },
            get_article() {
                var _this = this;
                var params = {};
                if (_this.search_word) {
                    params.search = _this.search_word;
                }
                {
                    (params.limit = _this.page.size), (params.offset = 0);
                }
                this.axios
                    .get("/api/v1/note_articles/", {
                        params: params,
                        headers: {
                            Authorization: "JWT ".concat(this.get_session_key("tools_token"))
                        }
                    })
                    .then(function (res) {
                        _this.article_list = res.data.results;
                        _this.page.total = res.data.count;
                        // console.log(_this.article_list);
                    });
            },
            handleSelect(key, keyPath) {
                var _this = this;
                var params = {};
                {
                    (params.category = key), (params.limit = _this.page.size), (params.offset = 0);
                }
                _this.axios
                    .get("/api/v1/note_articles/", {
                        params: params,
                        headers: {
                            Authorization: "JWT ".concat(this.get_session_key("tools_token"))
                        }
                    })
                    .then(function (res) {
                        _this.article_list = res.data.results;
                        _this.page.total = res.data.count;
                        _this.page.category = key;
                    });
            },
            handleCurrentChange(val) {
                var _this = this;
                var params = {};
                if (_this.page.category != 0) {
                    params.category = _this.page.category;
                }
                if (_this.search_word) {
                    params.search = _this.search_word;
                }
                {
                    (params.limit = _this.page.size),
                        (params.offset = _this.page.size * (val - 1));
                }

                _this.axios
                    .get("/api/v1/note_articles/", {
                        params: params,
                        headers: {
                            Authorization: "JWT ".concat(this.get_session_key("tools_token"))
                        }
                    })
                    .then(function (res) {
                        _this.article_list = res.data.results;
                        _this.page.total = res.data.count;
                    });
            },
            handleSizeChange(val) {
                var _this = this;
                var params = {};

                if (_this.search_word) {
                    params.search = _this.search_word;
                }else if (_this.page.category != 0) {
                    params.category = _this.page.category;
                }

                {
                    (params.limit = val), (params.offset = _this.page.offset);
                }
                _this.axios
                    .get("/api/v1/note_articles/", {
                        params: params,
                        headers: {
                            Authorization: "JWT ".concat(this.get_session_key("tools_token"))
                        }
                    })
                    .then(function (res) {
                        _this.article_list = res.data.results;
                        _this.page.total = res.data.count;
                        _this.page.size = val;
                    });
            }
        }
    };
</script>

<style>
  * {
    margin: 0;
    padding: 0;
  }

  a {
    text-decoration: none;
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

  @media (max-width: 575.98px) {
    .el-header {
      background-color: #b3c0d1;
      color: #333;
      /*height: 120px !important;*/
      /*line-height: 120px !important;*/
      height: auto !important;
      padding: 0 5px;
    }

    .el-header .search .el-input {
      width: 180px;
    }
  }

  @media (min-width: 576px) {
    .el-header {
      background-color: #b3c0d1;
      color: #333;
      line-height: 60px;
      padding-left: 10px;
    }

    .el-header .search .el-input {
      width: 240px;
    }
  }


  .logo {
    float: left;
    text-align: center;
    line-height: 60px;
  }

  .search {
    float: right;
    margin-right: 5px;
    line-height: 60px;
  }

  .search .el-button + .el-button {
    margin: 0px !important;
  }

  .input-with-select .el-input-group__prepend {
    background-color: #fff;
  }

  .el-aside {
    height: 100%;
    background-color: #d3dce6;
    color: #333;
    text-align: left;
  }

  .buttonText {
    display: block;
  }
</style>
