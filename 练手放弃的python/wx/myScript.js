function myFunction1() {
    window.alert("警告")
}
function myFunction2() {
    var str=document.getElementById('re').innerHTML;
    // var tex = str.replace(/jrfdalk/,"12345");
    document.getElementById('re').innerHTML=str.replace(/jrfdalk/,"12345");
}

var add = (function () {
    var counter = 0;
    return function () {return counter += 1}
})();
function myFunction3() {
    document.getElementById("demo3").innerHTML = add();

}
function myFunction4() {
    document.getElementsByClassName("demo5").innerHTML="主机"+location.pathname;
}