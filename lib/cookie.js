function SetCookie(name, value)//两个参数，一个是cookie的名子，一个是值
{
  var Days = 0.25; //此 cookie 将被保存 10 天
  var exp = new Date();    //new Date("December 31, 9998");
  exp.setTime(exp.getTime() + Days * 24 * 60 * 60 * 1000);
  document.cookie = name + "=" + escape(value) + ";expires=" + exp.toGMTString();
}
function getCookie(name)//读取cookies函数        
{
  var arr = document.cookie.match(new RegExp("(^| )" + name + "=([^;]*)(;|$)"));
  if (arr != null) return unescape(arr[2]); return null;
}
function delCookie(name)//删除cookie
{
  var exp = new Date();
  exp.setTime(exp.getTime() - 1);
  var cval = getCookie(name);
  if (cval != null) document.cookie = name + "=" + cval + ";expires=" + exp.toGMTString();
}

/*
$(function(){
  //获取存在cookie，并验证用户
  var username=getCookie("username");
  var login_path='/note/login.html';
  if (document.location.pathname!=login_path){
    if(username){
      $.get("/note/op.php",{action:"get_user",username:username},function(data){
        if(username!=JSON.parse(data)){
          window.location.href = login_path; 
        }
      })
    }else{
      window.location.href = login_path; 
    }
  }
})
*/
