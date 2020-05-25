export const editor = {
  methods: {
    getTreeData(data) {
      var _this = this;
      // 循环遍历json数据
      for (var i = 0; i < data.length; i++) {
        if (!data[i].hasOwnProperty("sub_cat") || data[i].sub_cat.length < 1) {
          // children若为空数组，则将children设为undefined
          data[i].sub_cat = undefined;
        } else {
          // children若不为空数组，则继续 递归调用 本方法
          _this.getTreeData(data[i].sub_cat);
        }
      }
      return data;
    }
    ,
    get_categorys() {
      var _this = this;
      this.axios
        .get("/api/v1/note_categorys/?type=1&format=json", {
          headers: {
            Authorization: "JWT ".concat(this.get_session_key("tools_token"))
          }
        })
        .then(function (res) {
          _this.cascader_data = _this.getTreeData(res.data);
          // console.log(_this.cascader_data);
        });
    },
  }
}
