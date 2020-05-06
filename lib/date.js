// 计算该年是否是闰年
function Is_RunYear(year){
  if (year%4==0&&year%100!=0||year%400==0){
    return true;
  }else{
    return false;
  }
}

// 计算该年的总天数
function get_DaysYear(year){
  return Is_RunYear(year)?366:365;
}

// 该日是该年的第几天
function get_DayOfYear1(y,m,d){
  var n_year=Number(y);
  var n_month=Number(m);
  var n_day=Number(d);
  var n_num=0;
  if(n_month==1){
    n_num=n_day;
  }else if(n_month==2){
    n_num=31+n_day;
  }else if(n_month==3){
    n_num=31+(Is_RunYear(n_year)?29:28)+n_day;
  }else if(n_month==4){
    n_num=31+(Is_RunYear(n_year)?29:28)+31+n_day;
  }else if(n_month==5){
    n_num=31+(Is_RunYear(n_year)?29:28)+31+30+n_day;
  }else if(n_month==6){
    n_num=31+(Is_RunYear(n_year)?29:28)+31+30+31+n_day;
  }else if(n_month==7){
    n_num=31+(Is_RunYear(n_year)?29:28)+31+30+31+30+n_day;
  }else if(n_month==8){
    n_num=31+(Is_RunYear(n_year)?29:28)+31+30+31+30+31+n_day;
  }else if(n_month==9){
    n_num=31+(Is_RunYear(n_year)?29:28)+31+30+31+30+31+31+n_day;
  }else if(n_month==10){
    n_num=31+(Is_RunYear(n_year)?29:28)+31+30+31+30+31+31+30+n_day;
  }else if(n_month==11){
    n_num=31+(Is_RunYear(n_year)?29:28)+31+30+31+30+31+31+30+31+n_day;
  }else if(n_month==12){
    n_num=31+(Is_RunYear(n_year)?29:28)+31+30+31+30+31+31+30+31+30+n_day;
  }
  // return n_year+"年"+n_month+"月"+n_day+"日"+"是"+n_year+"年的第"+n_num+"天";
  return n_num;
}

function get_DayOfYear2(y,m,d){
  var y=Number(y);m=Number(m);d=Number(d);
  var total=0;
  var arr=new Array(31,Is_RunYear(y)?29:28,31,30,31,30,31,31,30,31,30,31);
  for(var i=0;i<m-1;i++){
    total+=arr[i];
  }
  if(d>arr[m-1]){
    total+=arr[m-1];
    return total;
  }else{
    total+=d;
    return total;
  }
}


// 该日是星期几. 1900.1.1是星期一
function get_WeekYear1(y,m,d){
  var y=Number(y);m=Number(m);d=Number(d);
  var totalDays=0;
  var i=1900;
  while(i<y){
    totalDays+=get_DaysYear(i);
    i++;
  }
  totalDays+=get_DayOfYear2(y,m,d);
  return totalDays%7;
}

// 该年
