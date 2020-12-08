import Vue from "vue";
import VueRouter from "vue-router";
import CryptoJS from "crypto-js";
import axios from "axios";
import VueAxios from "vue-axios";

import {
  Container,
  Header,
  Aside,
  Main,
  Input,
  Button,
  ButtonGroup,
  Menu,
  Submenu,
  MenuItem,
  Table,
  TableColumn,
  Link,
  Cascader,
  Message,
  Pagination,
  Switch,
  Tooltip
} from "element-ui";

Vue.use(Container);
Vue.use(Header);
Vue.use(Aside);
Vue.use(Main);
Vue.use(Input);
Vue.use(Button);
Vue.use(ButtonGroup)
Vue.use(Menu);
Vue.use(Submenu);
Vue.use(MenuItem);
Vue.use(Table);
Vue.use(TableColumn);
Vue.use(Link);
Vue.use(Cascader);
Vue.use(Pagination);
Vue.use(Switch);
Vue.use(Tooltip);
Vue.config.productionTip = false;

Vue.prototype.$message = Message;
Vue.use(VueAxios, axios);

Vue.prototype.$CryptoJS = CryptoJS;
Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Index",
    component: resolve => require(["../views/Element.vue"], resolve),
    meta: {
      title: "Article List"
    }
  },
  {
    path: "/add",
    name: "Element_add",
    component: resolve => require(["../views/Element_add.vue"], resolve),
    meta: {
      title: "Article Add"
    }
  },
  {
    path: "/edit",
    name: "Element_edit",
    component: resolve => require(["../views/Element_edit.vue"], resolve),
    meta: {
      title: "Article Edit"
    }
  }
];

const router = new VueRouter({
  mode: "hash",
  base: process.env.BASE_URL,
  routes
});

export default router;
