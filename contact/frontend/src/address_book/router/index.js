import Vue from 'vue'
import VueRouter from 'vue-router'
import axios from "axios";
import VueAxios from "vue-axios";
import Home from '../views/Home.vue'

Vue.use(VueAxios, axios);
Vue.use(VueRouter)


const routes = [
    {
        path: '/',
        name: 'Home',
        component: Home
        // component: () => import(/* webpackChunkName: "about" */ '../views/Home.vue')
    }
]

const router = new VueRouter({
    mode: 'history',
    base: process.env.BASE_URL,
    routes
})

export default router
