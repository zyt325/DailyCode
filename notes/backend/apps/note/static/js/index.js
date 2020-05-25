//<script type="text/javascript">
debug=false;
function update_div_style(){
    // div list height
    var container = document.getElementById('container');
    container.style.width = window.innerWidth * 0.9 + 'px';
    container.style.marginLeft = 'auto';
    container.style.marginRight = 'auto';

    var article_list = document.getElementById('article_list');
    var article_header = document.getElementById('article_header');

    //console.log(article_list.scrollHeight);
    total_height=article_list.scrollHeight+article_header.scrollHeight;

    //console.log(total_height);
    if( total_height> window.innerHeight){
        container.style.height=total_height   +'px';
    }else{
        container.style.height = window.innerHeight * 1 + 'px';
    }
    article_list.style.borderLeftWidth='1px';
    article_list.style.borderLeftColor='#fff';
    article_list.style.borderLeftStyle='solid';
}

function getSearch(search_word,page){
    var xhr=CreateXhr();

    xhr.open('GET',"list/?search_word="+search_word+"&page="+page);
    xhr.send();
    xhr.onreadystatechange = function(){
        if(xhr.readyState==4 && xhr.status==200){
            result=xhr.responseText;
            // console.log(result);
            article_list_output(result);
        }
    }
}

// 获取分类和子分类的文章
function get_Aritlce_List(class_id,page){
    var xhr=CreateXhr();
    xhr.open('GET',"list/?class_id="+class_id+"&page="+page);
    xhr.send();
    xhr.onreadystatechange = function(){
        if(xhr.readyState==4 && xhr.status==200){
            result=xhr.responseText;
            article_list_output(result);
        }
    }
    update_div_style();
}

function article_list_output(result){
    var article_List="";
    var result=JSON.parse(result);
    var data=JSON.parse(result['data']);

    var article_list=document.getElementById("article_list")
    article_List=article_List+"<table>"
    for(var i in data){
        var article_title=data[i]['fields']['article_name'];
        var article_url="/media/articles/"+data[i]['fields']["file_name"];
        article_List=article_List+"<tr><td><span class=\"article\"><a target=\"_blank\" article_id=\""+i+"\"href=\""+article_url+"\">"+article_title+"</a></span></td>";
        // article_List=article_List+"<td><span class=\"article_mod\"><button onclick=\"article_edit(this)\" article_id=\""+i+"\">Edit</button></span></td></tr>";  //去掉编辑按钮
        article_List=article_List+"</tr>"
    }
    article_List=article_List+"</table>"

    // console.log(article_List);
    article_list.innerHTML=article_List;

    var article_page=document.getElementById("article_page");
    if(result['page']){
        var page_content="";
        page_content=page_content+"<table><tr><td><div class=\"pagination\"><span class=\"step-links\">";
        if(result['search_word']){
            if(result['page']['prev_page']){
                page_content=page_content+"<input type=\"button\" onclick=javascript:getSearch(\'"+result['search_word']+"\',"+1+") value=\"\&laquo\;\">";
                page_content=page_content+"<input type=\"button\" onclick=javascript:getSearch(\'"+result['search_word']+"\',"+result['page']['prev_page']+") value=\"prev\">";
            }
            page_content=page_content+"<span class=\"current\">Page "+result['page']['cur_page']+" of "+ result['page']['num_pages']+". ";
            if(result['page']['next_page']){
                page_content=page_content+"<input type=\"button\" onclick=javascript:getSearch(\'"+result['search_word']+"\',"+result['page']['next_page']+") value=\"next\">";
                page_content=page_content+"<input type=\"button\" onclick=javascript:getSearch(\'"+result['search_word']+"\',"+result['page']['num_pages']+") value=\"\&raquo\;\">";
            }
        }else{
            if(result['page']['prev_page']){
                page_content=page_content+"<input type=\"button\" onclick=javascript:get_Aritlce_List("+result['class_id']+","+1+") value=\"\&laquo\;\">";
                page_content=page_content+"<input type=\"button\" onclick=javascript:get_Aritlce_List("+result['class_id']+","+result['page']['prev_page']+") value=\"prev\">";
            }
            page_content=page_content+"<span class=\"current\">Page "+result['page']['cur_page']+" of "+ result['page']['num_pages']+". ";
            if(result['page']['next_page']){
                page_content=page_content+"<input type=\"button\" onclick=javascript:get_Aritlce_List("+result['class_id']+","+result['page']['next_page']+") value=\"next\">";
                page_content=page_content+"<input type=\"button\" onclick=javascript:get_Aritlce_List("+result['class_id']+","+result['page']['num_pages']+") value=\"\&raquo\;\">";
            }
        }

        page_content=page_content+"</span></div></td></tr></table>"
        article_page.innerHTML=page_content;
        article_page.style.display='block';
    }else{
        article_page.style.display='none';
    }
}

function addEvent_getArticle(classname,event){
  var class_obj=document.getElementsByClassName(classname);
  for (var i = 0; i < class_obj.length; i++) {
    class_obj[i].addEventListener(event,function(){
      class_id=this.getAttribute('class_id');
      get_Aritlce_List(class_id,1);
    })
  }
}

function addEvent_searchtext(){
    document.onkeypress=function () {
        var oEvent=window.event;
        // console.log(oEvent);
        if(oEvent.code == 'Enter' && oEvent.keyCode == 13){
            getSearch(document.getElementById('searchtext').value,1)
        }
    }
}

addEvent_selected("class0","click");
addEvent_getArticle("class0","click");
addEvent_getArticle("class1","click");
update_div_style();
addEvent_searchtext();






//</script>