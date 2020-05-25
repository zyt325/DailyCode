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
      <!-- 运维类 -->
      <div class="row body container tab-pane fade" id="OP">
        <div v-for="cat in tool_urls">
          <div v-if="cat.parent_category !== null">
            <div v-if="cat.parent_category.name == 'OP'">
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
      <!--  软件列表      -->
      <div class="row body container tab-pane fade" id="SOFT">
        <div v-for="cat in tool_urls">
          <div v-if="cat.parent_category !== null">
            <div v-if="cat.parent_category.name == 'SOFT'">
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

      <!-- 网址导航 -->
      <div class="row body container tab-pane active" id="URL">
        <div v-for="cat in tool_urls">
          <div v-if="cat.parent_category !== null">
            <div v-if="cat.parent_category.name == 'URL'">
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
                tool_urls: [],
                api_token: '',
            }
        },
        mounted() {
            var _this = this;
            const customLocalStorage = {
                set: function (key, value, ttl_s) {
                    var ttl_ms = Date.now() + 1000 * 60 * ttl_s;
                    var data = {value: value, expirse: new Date(ttl_ms).getTime()};
                    localStorage.setItem(key, JSON.stringify(data));
                },
                get: function (key) {
                    var data = JSON.parse(localStorage.getItem(key));
                    if (data !== null) {
                        //debugger
                        if (data.expirse != null && data.expirse < new Date().getTime()) {
                            localStorage.removeItem(key);
                        } else {
                            return data.value;
                        }
                    }
                    return null;
                }
            }

            function get_token() {
                _this.axios.post('/api/token-manual/', {
                        username: 'test',
                        password: _this.$CryptoJS.AES.encrypt('test6666', 'tools').toString()
                        // 'password': 'test6666'
                    },
                    {
                        headers: {
                            'Content-Type': 'application/json'
                        },
                    })
                    .then(function (response) {
                        customLocalStorage.set('tools_token', response.data.token, 5); //one day
                        _this.api_token = response.data.token;
                        get_url_data()
                    })
            }

            function get_url_data() {
                _this.axios.get('/api/v1/tool_categorys/?format=json&ordering=id', {
                    'headers': {
                        'Authorization': 'JWT '.concat(customLocalStorage.get('tools_token'))
                    }
                })
                    .then(function (res) {
                        _this.tool_urls = res.data;
                    })
            }

            _this.api_token = customLocalStorage.get('tools_token');
            if (!_this.api_token) {
                get_token();
            } else {
                get_url_data();
            }
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
