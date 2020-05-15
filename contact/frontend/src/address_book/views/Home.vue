<template>
    <a-layout id="components-layout-demo-fixed-sider">
        <a-layout-sider theme="dark" :style="{ overflow: 'auto', height: '100vh', position: 'fixed', left: 0 }">
            <a-menu mode="inline" theme="dark" :open-keys="openKeys" @openChange="onOpenChange" @click="HandlerClick">
                <a-sub-menu key="CITY">
                    <span slot="title">Cities</span>
                    <template v-for="c in citys">
                        <a-sub-menu v-if="c !== 'LA'" :key="c" :title="c" @titleClick="HandlerTitleClick">
                            <template v-for="d in city_deps">
                                <a-menu-item :key="d">
                                    {{ c }}-{{ d }}
                                </a-menu-item>
                            </template>
                        </a-sub-menu>
                    </template>
                </a-sub-menu>
                <a-sub-menu key="DEP">
                    <span slot="title">Departments</span>
                    <template v-for="d in deps">
                        <a-menu-item :key="d">
                            {{ d }}
                        </a-menu-item>
                    </template>
                </a-sub-menu>
            </a-menu>
        </a-layout-sider>
        <a-layout :style="{ marginLeft: '200px' ,height:'100vh'}">
            <template v-for="l in people">
                <h3 class="text-left">{{l.key}} - {{l.dep.code}} - {{l.dep.english_name}} -
                    {{l.dep.chinese_name}}</h3>
                <table class="table table-bordered">
                    <thead class="thead-light">
                    <tr>
                        <th scope="col" style="text-align: center;">Picture<br>照片</th>
                        <th scope="col" style="text-align: center;">Name名字<br>Company公司</th>
                        <th style="text-align: center;">Title<br>职位</th>
                        <th style="text-align: center;">Phone<br>电话</th>
                        <th style="text-align: center;">Office_Phone<br>办公电话</th>
                        <th style="text-align: center;">Email<br>邮件</th>
                        <th style="text-align: center;">Chat<br>即时消息</th>
                        <th style="text-align: center;">Wechat<br>微信</th>
                        <th style="text-align: center;">Seat<br>座位图</th>
                    </tr>
                    </thead>
                    <tbody>
                    <template v-for="p in l.value">
                        <tr>
                            <td>
                                <div class="content-wrapper">
                                    <p>
                                        <a :href="'https://hr.base-fx.com/index.php/api/staffPhoto/username/'+p.username"
                                           target="_blank">
                                            <img height="105px"
                                                 :src="'https://hr.base-fx.com/index.php/api/staffPhoto/username/'+p.username+'/width/200/height/200'">
                                        </a>
                                    </p>
                                </div>
                            </td>
                            <template v-if="p.gender=='F'">
                                <td class="bg-F" style="text-align: center;">
                                    <span style="color: rgb(0,0,0);">{{p.first_name}} {{p.last_name}}</span>
                                    <br style="text-align: center;"/>
                                    <span style="color: rgb(0,0,0);">{{p.chinese_name}}</span>
                                    <br style="text-align: center;"/>
                                    <span style="color: rgb(0,0,0);">{{p.code}}</span>
                                    <br style="text-align: center;"/>
                                    <template v-if="p.attendance">
                                        <a><img src="https://inventory.base-fx.com/Public/Inventory/img/yes.png"
                                                title="Clocked in"/></a>
                                    </template>
                                    <template v-else>
                                        <a><img src="https://inventory.base-fx.com/Public/Inventory/img/no.png"
                                                title="Did not clock in"/></a>
                                    </template>
                                </td>
                            </template>
                            <template v-else>
                                <td class="bg-M" style="text-align: center;">
                                    <span style="color: rgb(0,0,0);">{{p.first_name}} {{p.last_name}}</span>
                                    <br style="text-align: center;"/>
                                    <span style="color: rgb(0,0,0);">{{p.chinese_name}}</span>
                                    <br style="text-align: center;"/>
                                    <span style="color: rgb(0,0,0);">{{p.code}}</span>
                                    <br style="text-align: center;"/>
                                    <template v-if="p.attendance">
                                        <a><img src="https://inventory.base-fx.com/Public/Inventory/img/yes.png"
                                                title="Clocked in"/></a>
                                    </template>
                                    <template v-else>
                                        <a><img src="https://inventory.base-fx.com/Public/Inventory/img/no.png"
                                                title="Did not clock in"/></a>
                                    </template>
                                </td>
                            </template>


                            <td style="text-align: center;">
                                  <span style="color: rgb(0,0,0);">{{p.title}}<br/>
                                    <span style="color: rgb(0,0,0);">{{p.title_cn}}</span>
                                  </span>
                            </td>
                            <td style="text-align: center;">
                                <span style="color: rgb(0,0,0);">{{p.mobile}}</span>
                            </td>
                            <td style="text-align: center;">
                                <span style="color: rgb(0,0,0);">{{p.phone}}</span>
                            </td>
                            <td style="text-align: center;">
                                <a href="mailto:%s">{{p.email}}</a>
                            </td>
                            <td style="text-align: center;">
                                <span style="color: rgb(0,0,0);">{{p.username}}</span>
                            </td>
                            <td style="text-align: center;">
                                <span style="color: rgb(0,0,0);">{{p.wechat}}</span>
                            </td>
                            <td style="text-align: center;">
                                <a :href="'https://seatmap.base-fx.com/index.php/employee/employee_edit/employee_id/'+p.id+'.html'"
                                   target="_blank"><img src="https://inventory.base-fx.com/Public/Inventory/img/map.png"
                                                        title="seatmap"/></a>
                            </td>
                        </tr>
                    </template>
                    </tbody>
                </table>
            </template>
        </a-layout>
    </a-layout>
</template>

<script>
    const columns = [{
        key: 'username',
        slots: {title: 'custompic'}
    }]
    export default {
        data() {
            return {
                rootSubmenuKeys: ['CITY', 'DEP'],
                openKeys: ['CITY','BJ'],
                citys: [],
                city_deps: [],
                people: [],
                deps: [],
            };
        },
        mounted() {
            this.get_city();
            this.get_deps();
            this.get_people_city('BJ');
        },
        methods: {
            onOpenChange(openKeys) {
                const latestOpenKey = openKeys.find(key => this.openKeys.indexOf(key) === -1);
                if (this.rootSubmenuKeys.indexOf(latestOpenKey) !== -1) {
                    this.openKeys = latestOpenKey ? [latestOpenKey] : [];
                } else if (this.citys.indexOf(latestOpenKey) !== -1) {
                    this.openKeys = ["CITY", latestOpenKey];
                } else {
                    this.openKeys = openKeys;
                }
                // console.log(openKeys, latestOpenKey, this.openKeys)
            },
            HandlerClick(openKeys) {
                // console.log(openKeys);
                var keypath = openKeys.keyPath;
                var keypath_parent = keypath[keypath.length - 1]
                var city = keypath[keypath.length - 2]
                var dep = openKeys.key
                if (keypath_parent == 'DEP') {
                    this.get_people_dep(openKeys);
                } else {
                    this.get_people_city_dep(city, dep)
                }
            },
            HandlerTitleClick(e) {
                // console.log(e)
                this.get_city_deps(e.key);
                this.get_people_city(e.key);
            },
            get_city() {
                var _this = this;
                _this.axios
                    .get("/api/city/")
                    .then(function (res) {
                        _this.citys = res.data;
                        // console.log(_this.citys);
                    });
            },
            get_city_deps(city) {
                var _this = this;
                _this.axios
                    .get("/api/city_dep/?city=" + city)
                    .then(function (res) {
                        _this.city_deps = res.data;
                        // console.log(_this.city_deps);
                    });
            },
            get_people_city(city) {
                var _this = this;
                _this.axios
                    .get("/api/people_city_dep/?city=" + city)
                    .then(function (res) {
                        _this.people = res.data;
                        // console.log(_this.people);
                    });
            },
            get_people_city_dep(city, dep) {
                var _this = this;
                _this.axios
                    .get("/api/people_city_dep/?city=" + city + "&dep=" + dep)
                    .then(function (res) {
                        _this.people = res.data;
                        // console.log(_this.people);
                    });
            },
            get_deps() {
                var _this = this;
                _this.axios
                    .get("/api/dep/")
                    .then(function (res) {
                        _this.deps = res.data;
                        // console.log(_this.deps);
                    });
            },
            get_people_dep(openKeys) {
                var _this = this;
                _this.axios
                    .get("/api/people_dep/?dep=" + openKeys.key)
                    .then(function (res) {
                        _this.people = res.data;
                        // console.log(_this.people);
                    });
            }
        },
    }
</script>

<style>
    @import url("/bootstrap.min.css");

    .ant-layout {
        background: #fff !important;
    }

    .ant-menu-submenu-title, .ant-menu-sub {
        text-align: left !important;
    }

    .bg-F {

        background-color: #ffe7e7 !important;
    }

    .bg-M {
        background-color: #e0f0ff !important;
    }
</style>