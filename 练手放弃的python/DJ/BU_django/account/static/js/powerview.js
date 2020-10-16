function arrChange( a, b ){
      for (var i = 0; i < b.length; i++) {
        for (var j = 0; j < a.length; j++) {
          if (a[ j ] == b[ i ]) {//如果是id相同的，那么a[ j ].id == b[ i ].id
            a.splice(j, 1);
            j = j - 1;
          }
        }
      }
      return a;
    }
if($.cookie('user')!='superadmin') {
    let paras = $.cookie('role');
    let paras1 = paras.replace('角色管理','role_off');
    let paras2 = paras1.replace('管理员管理','admin_off');
    let paras3 = paras2.replace('资费管理','fee_off');
    let paras4 = paras3.replace('账务账号','account_off');
    let paras5 = paras4.replace('业务账号','service_off');
    let paras6 = paras5.replace('账单管理','bill_off');
    let paras7 = paras6.replace('报表','report_off');
    b = paras7.split(',');
    var a = ["role_off", "admin_off", "fee_off", "account_off", "service_off", "bill_off", "report_off"];
    arrChange(a,b);
    for(i=0; i<=a.length-1; i++){
        let par = a[i];
        $('.y'.replace('y',par)).css({
            display:'none'
        })
    }
    $('#menu li').css({
        padding:'0'
    })

}
