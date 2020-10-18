/* 初始化markdown编辑器  */
var AritcleHeight=window.innerHeight * 0.85 + 'px';
var ArticleTxt;

function getQueryString(name) {
  var reg = new RegExp("(^|&)" + name + "=([^&]*)(&|$)", "i");
  var r = window.location.search.substr(1).match(reg);
  if (r != null) return unescape(r[2]);
  return null;
}

$(function () {
  ArticleTxt = editormd("ArticleTxt", {
    width: "90%",
    height: AritcleHeight,
    markdown: "",
    // syncScrolling: "single",
    path: "http://module.personer.website/editor.md/lib/", //你的path路径（原资源文件中lib包在我们项目中所放的位置）

    placeholder: '本编辑器支持Markdown编辑，左边编写，右边预览',

    // 编辑器主题
    // theme: "dark", //工具栏主题
    // previewTheme: "dark", //预览主题
    // editorTheme: "pastel-on-dark", //编辑主题

    // 图片上传
    imageUpload: true,
    imageFormats: ["jpg","jpeg","gif","png"],
    imageUploadURL: "/upload/",
    /*
    上传的后台只需要返回一个 JSON 数据，结构如下：
    {
      success : 0 | 1,           // 0 表示上传失败，1 表示上传成功
      message : "提示的信息，上传成功或上传失败及错误信息等。",
      url     : "图片地址"        // 上传成功时才返回
    }
    */

    saveHTMLToTextarea: true,
    emoji: true,
    taskList: true,
    tocm: true, // Using [TOCM]
    tex: true, // 科学公式TeX语言支持，默认关闭
    flowChart: false, // 流程图支持，默认关闭
    sequenceDiagram: false, // 时序/序列图支持，默认关闭,
    toolbarIcons: function () { //自定义工具栏，后面有详细介绍
      return editormd.toolbarModes['full']; // full, simple, mini
       // Using "||" set icons align right.
       // return ["undo", "redo", "|", "bold", "hr", "|", "preview", "watch", "|", "fullscreen", "info", "testIcon", "testIcon2", "file", "faicon", "||", "watch", "fullscreen", "preview", "testIcon"]
    },

    /* 编辑器ajax获取需要编辑的内容 */
    onload:function(){
      var xhr=CreateXhr();
      var article_id='';
      var article_List=""
      article_id=getQueryString('id');
      xhr.open("GET","/get/?id="+article_id);
      xhr.send();
      xhr.onreadystatechange = function(){
        if(xhr.readyState==4 && xhr.status==200){
          result=xhr.responseText;
          var result=JSON.parse(result);
          document.getElementById("ArticleTitle").value=result['title'];
          ArticleTxt.setMarkdown(result['body']);
          article_title_old=result['title'];
        }
      }
    }
  });
  //testEditor.getMarkdown();
  // 在js中调用getMarkdown这个方法可以获得Markdown格式的文本。

});
//标题提醒，替换
function title_warn(warn_elem,warn_txt){
  var old_elem=warn_elem.nextSibling
  var artitle_title_warn=document.createElement('span');
  artitle_title_warn.innerText=warn_txt;
  artitle_title_warn.style.color='blue';
  warn_elem.style.borderColor='red';
  warn_elem.style.borderWidth='2px';
  warn_elem.parentNode.replaceChild(artitle_title_warn,old_elem)
}

/* 提交markdown内容、标题、分类  */
var artitle_title=document.getElementById("ArticleTitle");
function submitTxt(){
  var secret=document.getElementById("secret");
  var classid=document.getElementById("ClassId");
  // 标题不能为空
  if(artitle_title.value==''){
    title_warn(artitle_title,"标题不能为空");
  }else{
    var SubmitTxt=document.getElementById("SubmitTxt");
    article_content=ArticleTxt.getMarkdown();
    article_content_html=ArticleTxt.getPreviewedHTML();
    var xhr=CreateXhr();
    xhr.open("POST","/edit/",true);
    xhr.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
    xhr.send("class_id="+encodeURIComponent(classid.value)+"&article_id="+encodeURIComponent(getQueryString('id'))+"&title="+encodeURIComponent(artitle_title.value)+"&body="+encodeURIComponent(article_content)+"&body_html="+encodeURIComponent(article_content_html)+"&secret="+encodeURIComponent(secret.value));
    xhr.onreadystatechange = function(){
      if(xhr.readyState==4 && xhr.status==200){
        result=JSON.parse(xhr.responseText);
        if(Object.prototype.toString.call(result) ===  "[object Object]" &&  result['status']==1){
          artitle_title.value='';
          ArticleTxt.setValue("");
          secret.value='';
          window.location.href = "/media/articles/"+result['result']['filename'];
        }else if(xhr.responseText==2){
          title_warn(artitle_title,"标题已经存在")
          secret.value='';
        }else if(xhr.responseText==3){
          title_warn(artitle_title,"操作密码错误")
          secret.value='';
        }else if(xhr.responseText==4){
          title_warn(artitle_title,"保存失败")
          secret.value='';
        }else if(xhr.responseText==0){
          alert("提交失败");
        }
      }
    }
  }
}