function getCurrentDate() {
	  var now = new Date();
	  var year = now.getFullYear(); //得到年份
	  var month = now.getMonth();//得到月份
	  var date = now.getDate();//得到日期
	  month = month + 1;
	  if (month < 10) month = "0" + month;
	  if (date < 10) date = "0" + date;
	  var time = "";
	  time = year + "-" + month + "-" + date+ " " ;
	  return time;
	}
	var nowtime = getCurrentDate();