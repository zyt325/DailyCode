<template>
  <div class="container-fluid">
    <div class="row header bg-light">
      <div class="row-12">
        <nav class="navbar navbar-expand-lg navbar-light font-weight-bold">
          <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarTools"
                  aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
          </button>
          <a class="navbar-brand" href="#">工具箱</a>
          <div class="collapse navbar-collapse" id="navbarTools">
            <ul class="navbar-nav mr-auto nav nav-tabs">
              <li class="nav-item"><a class="nav-link" data-toggle="tab" href="#DEV">开发类<span
                class="sr-only">(current)</span></a></li>
              <li class="nav-item"><a class="nav-link" data-toggle="tab" href="#OP">运维类<span
                class="sr-only">(current)</span></a></li>
              <li class="nav-item"><a class="nav-link" data-toggle="tab" href="#SOFT">软件类<span
                class="sr-only">(current)</span></a></li>
              <li class="nav-item active"><a class="nav-link active" data-toggle="tab" href="#URL">网址导航<span
                class="sr-only">(current)</span></a></li>
            </ul>
          </div>
        </nav>
      </div>
    </div>
    <div class="tab-content">
      <!-- 开发类 -->
      <div class="row body container tab-pane fade" id="DEV">
        <div v-for="cat in tool_urls">
          <div v-if="cat.parent_category !== null">
            <div v-if="cat.parent_category.name == 'DEV'">
              <div class="col-sm-12">
                <div class="row">
                  <div class=" col-sm-1 font-weight-bold">{{ cat.name }}</div>
                  <div class="col-sm-11">
                    <div class="card" v-for="url in cat.urls">
                      <div class="card-body">
                        <a :href="url.url" target="_blank" class="card-link">{{ url.name }}</a>
                      </div>
                    </div>
                  </div>
                </div>
                <p></p>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!-- 运维类 -->
      <div class="row body container tab-pane fade" id="OP">
        <div v-for="cat in tool_urls">
          <div v-if="cat.parent_category !== null">
            <div v-if="cat.parent_category.name == 'OP'">
              <div class="col-sm-12">
                <div class="row">
                  <div class=" col-sm-1 font-weight-bold">{{ cat.name }}</div>
                  <div class="col-sm-11">
                    <div class="card" v-for="url in cat.urls">
                      <div class="card-body">
                        <a :href="url.url" target="_blank" class="card-link">{{ url.name }}</a>
                      </div>
                    </div>
                  </div>
                </div>
                <p></p>
              </div>
            </div>
          </div>
        </div>
      </div>
      <!--  软件列表      -->
      <div class="row body container tab-pane fade" id="SOFT">
        <div v-for="cat in tool_urls">
          <div v-if="cat.parent_category !== null">
            <div v-if="cat.parent_category.name == 'SOFT'">
              <div class="col-sm-12">
                <div class="row">
                  <div class=" col-sm-1 font-weight-bold">{{ cat.name }}</div>
                  <div class="col-sm-11">
                    <div class="card" v-for="url in cat.urls">
                      <div class="card-body">
                        <a :href="url.url" target="_blank" class="card-link">{{ url.name }}</a>
                      </div>
                    </div>
                  </div>
                </div>
                <p></p>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 网址导航 -->
      <div class="row body container tab-pane active" id="URL">
        <div v-for="cat in tool_urls">
          <div v-if="cat.parent_category == null">
            <div class="btn-group-vertical" role="group" aria-label="Vertical button group" v-if="cat.name == 'URL'">
              <div v-for="sub in cat.sub_cat">
                <button type="button" class="btn btn-light"><a v-bind:href="'#'+sub.name">{{sub.name}}</a></button>
              </div>
            </div>
          </div>
          <div v-else-if="cat.parent_category.name == 'URL'">
            <div class="col-sm-12">
              <div class="row">
                <div class=" col-sm-1 font-weight-bold" :id="cat.name"></div>
                <div class="col-sm-11">
                  <div class="card" v-for="url in cat.urls">
                    <div class="card-body">
                      <a :href="url.url" target="_blank" class="card-link">{{ url.name }}</a>
                    </div>
                  </div>
                </div>
              </div>
              <p></p>
            </div>
          </div>
          <div v-else></div>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
    import 'bootstrap/dist/css/bootstrap.min.css'
    import 'jquery/dist/jquery.min.js'
    import 'popper.js/dist/umd/popper.min.js'
    import 'bootstrap/dist/js/bootstrap.min.js'

    export default {
        name: 'Tools',
        data() {
            return {
                msg: 'Welcome to Your Vue.js App',
                tool_urls: []
            }
        },
        mounted() {
            var _this = this;
            _this.axios.get('/api/v1/tool_categorys/?format=json&ordering=id')
                .then(function (res) {
                    _this.tool_urls = res.data;
                })
        }
    }
</script>

<style>
  /* Small devices (landscape phones, 576px and up) */
  @media (min-width: 576px) {
    .body .card {
      width: calc(100% - 24px);
    }
  }

  /* Medium devices (tablets, 768px and up) */
  @media (min-width: 768px) {
    .body .card {
      float: left;
      width: 50%;
    }
  }

  /* Large devices (desktops, 992px and up) */
  @media (min-width: 992px) {
    .body .card {
      float: left;
      width: 25%;
    }
  }

  /* Extra large devices (large desktops, 1200px and up) */
  @media (min-width: 1200px) {
    .body .card {
      float: left;
      width: 20%;
    }
  }
</style>
