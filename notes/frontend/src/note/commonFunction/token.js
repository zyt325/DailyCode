export const token = {
  methods: {
    set_session_key(key, value, ttl_s) {
      var ttl_ms = Date.now() + 1000 * 60 * ttl_s;
      var data = {value: value, expirse: new Date(ttl_ms).getTime()};
      sessionStorage.setItem(key, JSON.stringify(data));
    },
    get_session_key(key) {
      var data = JSON.parse(sessionStorage.getItem(key));
      if (data !== null) {
        //debugger
        if (data.expirse != null && data.expirse < new Date().getTime()) {
          sessionStorage.removeItem(key);
        } else {
          return data.value;
        }
      } else {
        this.get_token();
      }
      return null;
    },
    get_token() {
      var _this = this;
      this.axios
        .post(
          "/api/token-manual/",
          {
            username: "test",
            password: this.$CryptoJS.AES.encrypt("test6666", "tools").toString()
            // 'password': 'test6666'
          },
          {
            headers: {
              "Content-Type": "application/json"
            }
          }
        )
        .then(function (response) {
          // console.log(response.data);
          _this.set_session_key("tools_token", response.data.token, 120);
          _this.get_category();
          _this.get_article();
          // return _this.get_session_key("tools_token");
          return response.data.token
        });
    }
  },

}
