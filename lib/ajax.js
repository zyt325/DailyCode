function CreateXhr(){
  var xhr;
  if(window.XMLHttpRequest){
    xhr = new XMLHttpRequest();
  }else{
    xhr = new ActiveXObject("Mirosoft.XMLHttp");
  }
  // xhr.setRequestHeader("Access-Control-Allow-Methods", "*");
  // xhr.setRequestHeader("Access-Control-Allow-Origin", "*");
  // xhr.setRequestHeader("Access-Control-Allow-Headers", "*");
  return xhr;
}

//open(method,url,async)    // async：true（异步）或 false（同步）
//send(string)	将请求发送到服务器。string：仅用于 POST 请求
// 示例-POST
/*
xhr.open("POST","/note/op.php",false);
xhr.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
xhr.send("action=get_user"+"&username="+username);
xhr.onreadystatechange = function(){
  if(xhr.readyState==4 && xhr.status==200){
    result=JSON.parse(xhr.responseText);
    console.log(0);
    if(!cmp(username,result)){
      console.log(1);
      window.location.href = login_path; 
    }
  }
}
*/
//示例-GET
/*
xmlhttp.open("GET","/try/ajax/demo_get.php?t=" + Math.random(),true);
xmlhttp.send();
xmlhttp.responseText;
*/