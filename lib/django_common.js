//list 选项功能
function getchecked(status,keys) { //
  var elements = document.getElementsByClassName(status); //获取input标签
  var dblist = {};
  var j = 0;
  for (var i = 0; i < elements.length; i++) { //根据标签的长度执行循环
    if (elements[i].type == 'checkbox') { //判断对象中元素的类型
      if (elements[i].checked == true) { //判断当checked的值为TURE时
        dblist[j]={};
        for(var m=0;m<keys.length;m++){
          k=keys[m];
          // console.log(k+elements[i][k]);
          dblist[j][k]=elements[i][k]; 
        }
        // dblist[j] = elements[i].id; //将checked赋值为FALSE
        j++;
      }
    }
  }
  if (dblist.length == 1) {
    return [dblist, dblist.length];
  } else {
    return [dblist, dblist.length];
  }
}

//全选、不选和反选功能
function uncheckAll(status) { //不选
  var elements = document.getElementsByClassName(status); //获取input标签
  for (var i = 0; i < elements.length; i++) { //根据标签的长度执行循环
    if (elements[i].type == 'checkbox') { //判断对象中元素的类型
      if (elements[i].checked == true) { //判断当checked的值为TURE时
        elements[i].checked = false; //将checked赋值为FALSE
      }
    }
  }
}

function checkAll(status) { //全选
  var elements = document.getElementsByClassName(status);
  for (var i = 0; i < elements.length; i++) {
    if (elements[i].type == 'checkbox') {
      if (elements[i].checked == false) {
        elements[i].checked = true;
      }
    }
  }
}

function switchAll(status) { //反选
  var elements = document.getElementsByClassName(status);
  for (var i = 0; i < elements.length; i++) {
    if (elements[i].type == 'checkbox') {
      if (elements[i].checked == true) {
        elements[i].checked = false;
      } else if (elements[i].checked == false) {
        elements[i].checked = true;
      }
    }
  }
}

function check_ip(ip) {
  var reSpaceCheck = /^(\d+)\.(\d+)\.(\d+)\.(\d+)$/;
  // =/^(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9])\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[1-9]|0)\.(25[0-5]|2[0-4][0-9]|[0-1]{1}[0-9]{2}|[1-9]{1}[0-9]{1}|[0-9])$/;
  if (reSpaceCheck.test(ip)) {
    ip.match(reSpaceCheck);
    if (RegExp.$1 <= 255 && RegExp.$1 >= 0 && RegExp.$2 <= 255 && RegExp.$2 >= 0 &&
      RegExp.$3 <= 255 && RegExp.$3 >= 0 && RegExp.$4 <= 255 && RegExp.$4 >= 0) {
      return true;
    } else {
      return false;
    }
  } else {
    return false;
  }
}

// 随机数
function genID(length) {
  return Number(Math.random().toString().substr(3, length) + Date.now()).toString(36);
}


// 给selected添加事件
function addEvent_selected(classname, event) {
  var class_obj = document.getElementsByClassName(classname);

  function class1_display() {
    for (var i = 0; i < class_obj.length; i++) {
      class_obj[i].style.backgroundColor = "#D4E6EB";
      if (class_obj[i].nextSibling) {
        class_obj[i].nextSibling.nextElementSibling.style.display = "none";
      }
    }
  }
  for (var i = 0; i < class_obj.length; i++) {
    class_obj[i].addEventListener(event, function () {
      if (this.nextSibling) {
        if (this.nextSibling.nextElementSibling.style.display == "none") {
          class1_display()
          this.nextSibling.nextElementSibling.style.display = "block";
          this.nextSibling.nextElementSibling.style.backgroundColor = "#93BFCC";
        } else {
          this.nextSibling.nextElementSibling.style.display = "none";
        }
      } else {
        class1_display();
      }
      this.style.backgroundColor = "#6B8D9D";
    })
  }
}

// cmp函数
cmp = function (x, y) {
  // If both x and y are null or undefined and exactly the same 
  if (x === y) {
    return true;
  }

  // If they are not strictly equal, they both need to be Objects 
  if (!(x instanceof Object) || !(y instanceof Object)) {
    return false;
  }

  //They must have the exact same prototype chain,the closest we can do is
  //test the constructor. 
  if (x.constructor !== y.constructor) {
    return false;
  }

  for (var p in x) {
    //Inherited properties were tested using x.constructor === y.constructor
    if (x.hasOwnProperty(p)) {
      // Allows comparing x[ p ] and y[ p ] when set to undefined 
      if (!y.hasOwnProperty(p)) {
        return false;
      }

      // If they have the same strict value or identity then they are equal 
      if (x[p] === y[p]) {
        continue;
      }

      // Numbers, Strings, Functions, Booleans must be strictly equal 
      if (typeof (x[p]) !== "object") {
        return false;
      }

      // Objects and Arrays must be tested recursively 
      if (!Object.equals(x[p], y[p])) {
        return false;
      }
    }
  }

  for (p in y) {
    // allows x[ p ] to be set to undefined
    if (y.hasOwnProperty(p) && !x.hasOwnProperty(p)) {
      return false;
    }
  }
  return true;
}

function loadScript(url) {
  var script = document.createElement("script");
  script.type = "text/javascript";
  script.src = url;
  document.body.appendChild(script);
}


//get url value
function getQueryString(name) {
  var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
  var r = window.location.search.substr(1).match(reg);
  if (r != null) return unescape(r[2]);
  return null;
}