import Vue from 'vue';
import VueRouter from 'vue-router';
import axios from 'axios';
import VueAxios from 'vue-axios';
import CryptoJS from 'crypto-js';

// import Tools from "../views/Tools";
// import Toolsv1 from '../views/Tools-v1';
const Tools = () => import(/* webpackChunkName: "group-tools" */'../views/Tools.vue');
const Toolsv1 = () => import(/* webpackChunkName: "group-tools" */'../views/Tools-v1.vue');

Vue.prototype.$CryptoJS = CryptoJS;
Vue.use(VueRouter);
Vue.use(VueAxios, axios);

const routes = [
  {
    path: '/',
    name: 'Tools',
    component: Tools,
    meta: {
      title: 'Tools'
    }
  },
  {
    path: '/v1',
    name: 'Toolsv1',
    component: Toolsv1,
    meta: {
      title: 'Toolsv1'
    }
  }
];

const router = new VueRouter({
  mode: 'hash',
  base: process.env.BASE_URL,
  routes
});

export default router
