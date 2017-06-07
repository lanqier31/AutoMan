// 重新执行测试脚本
function ajaxReRun(){
  var select = document.getElementById("project_version");
  var options = select.options;
  var index = select.selectedIndex;
  var version_text = options[index].text;
  $.ajax({
    //提交数据的类型 POST GET
    type:"POST",
    //提交的网址
    url:"/redo",
    //提交的数据
    data:({"selected_version": version_text}),
    //返回数据的格式 "xml", "html", "script", "json", "jsonp", "text"
    datatype: "text",
	//ajax请求成功后的事件
    success:function(data){
        if (data=='environment is not exist'){
            alert("亲~  这个版本的测试环境去哪儿了？");
        }
        else{
            window.location.href =  window.location.href;
            alert("所选版本的前端性能测试执行完毕");
        }

    },

    //调用出错执行的函数
    error: function(XMLResponse){
        //请求出错处理
	    alert("不要搞事情~ 请cc检查服务是否开启");
    }
  });
}


//实例化汇总表格
var TableInit=function(){
  
  
  //初始化Table
  this.Init=function(){
    $('#pages_summary').bootstrapTable({
        method:'post',
        toolbar:'#toolbar',
        data:this.data,
        dataType:'json',
        striped:false,  //是否行间隔色显示
        cache:false,//是否试用缓存，默认为true
        pagination:true, //s是否分页
        sortable:true,  //是否启用排序
        sortOrder:"page_name asc", // 排序方式
        pageNumber:1, //初始化加载第一页，默认第一页
        pageSize:10 , //每页的记录行数
        // pageList:[6,20,50] ,  //可供选择的每页行数
        // url:'/webloadlist',
        queryParamsType:'', //默认为limit， 在默认情况下，传给服务器的参数为；offset，limit， 设置为''则传给服务器的参数为pageSize，pageNumber
        sidePagination:"client",// 分页方式，client为客户端分页，server为服务端分页
        strictSearch:true,
        clickToSelect:true,  //是否启动点击选中行
        
        search:false,
        // height:$(window).height() - 500,
        columns:[
          
              { 
                title:"",
                field:'state',
                checkbox:true,
                align:'center',
                valign:'middle'
              },{
                title:'Name',
                field:'page_name',
                align:'left',
                valign:'middle',
                sortable:true,
                class:'text-overflow',
                width:120,
                formatter: 'actionFormatter',
                events:'onclick'
              
              },{
                title:'Urls',
                field:'url',
                width:450,
                align:'left',
                valign:'middle',
                class:'text-overflow',
                switchable:true
                
                
              },{
                title:'加载总耗时(ms)',
                field:'loadall',
                align:'center',
                valign:'middle',
                sortable:true,
                switchable:true

              },{
                title:'DNS耗时',
                field:'dns',
                align:'center',
                valign:'middle',
                sortable:true

              },{
                title:'白屏时长',
                field:'whitewait',
                align:'center',
                valign:'middle',
                sortable:true
              },{
                title:'Request耗时',
                field:'request',
                align:'center',
                valign:'middle',
                sortable:true
              },{
                title:'domReady耗时',
                field:'dom_ready',
                align:'center',
                valign:'middle',
                switchable:false,
                sortable:true

              },{
                title:'loadEvent耗时',
                field:'load_event',
                align:'center',
                valign:'middle',
                sortable:true

              },{
                title:'是否重定向',
                field:'ifredirect',
                
                align:'center',
                valign:'middle',
                sortable:true
                
              }
            
            ],
        showColumns:true,   // 是否显示列
        minimumCountColumns:2,
        showRefresh:true,  // 是否刷新
        showToggle:true,

    });
  };
  //销毁表格
  this.Destory = function(){
    $('#pages_summary').bootstrapTable('destroy');
  };
}

//执行测试用例
function doUItest(){
  var version_text = $('#project_version').find("option:selected").text();
  var testsuite=$('#testsuite').find("option:selected").text();
  var subsuite=$('#subtestsuite').find("option:selected").text();
  alert(subsuite )
  $.ajax({
                //提交数据的类型 POST GET
                type:"POST",
                //提交的网址
                url:"/uitest_operate",
                async:false,
                //提交的数据
                data:{"select_version":version_text,"testsuite":testsuite,"subsuite": subsuite},
                //返回数据的格式 "xml", "html", "script", "json", "jsonp", "text"
                datatype: "json",
                //ajax请求成功后的事件
                success:function(data){     
                    $('#suite').html($(data).find('#suite').html());                
                },
                //调用出错执行的函数
                error: function(XMLResponse){
                    //请求出错处理
                    alert("不存在该测试用例");
                },
            });
}



