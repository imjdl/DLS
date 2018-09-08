function getXmlHttp() {
    var xmlhttp;
    if (window.XMLHttpRequest) {
        //  IE7+, Firefox, Chrome, Opera, Safari 浏览器执行代码
        xmlhttp=new XMLHttpRequest();
    }
    else {
        // IE6, IE5 浏览器执行代码
        xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }
    return xmlhttp;
}

function strtojson(str) {
    var json = (new Function("return " + str))();
    return json;
}

function getLogdata() {
    var xmlhttp = getXmlHttp();
    var csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    xmlhttp.open("POST",'/index/getdata', true);
    xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
    var data = "csrfmiddlewaretoken=" + csrf;
    xmlhttp.send(data)
    xmlhttp.onreadystatechange = function() {
        var data = strtojson(xmlhttp.responseText).logdata;
        if(data == '[]'){
            console.log(123);
        }else {
            console.log(data);
        }
    }

}

var handler = setInterval(getLogdata, 1000);
