//$(function	()	{
/*
  	//Flot Chart (Total Sales)
	var d1 = [];
	for (var i = 0; i <= 10; i += 1) {
		//d1.push([i, parseInt(Math.random() * 30)]);
		d1 = [[0,700],[1,1200],[2,1100],[3,900],[4,500],[5,700],[6,500],[7,600],[8,1200],[9,1700],[10,1200]];
	}*/
/*
	function plotWithOptions() {
		$.plot("#placeholder", [d1], {
			series: {
				lines: {
					show: true,
					fill: true,
					fillColor: '#eee',
					steps: false,
					
				},
				points: { 
					show: true, 
					fill: false 
				}
			},

			grid: {
				color: '#fff',
				hoverable: true,
    			autoHighlight: true,
			},
			colors: [ '#bbb'],
		});
	}

	$("<div id='tooltip'></div>").css({
		position: "absolute",
		display: "none",
		border: "1px solid #222",
		padding: "4px",
		color: "#fff",
		"border-radius": "4px",
		"background-color": "rgb(0,0,0)",
		opacity: 0.90
	}).appendTo("body");

	$("#placeholder").bind("plothover", function (event, pos, item) {

		var str = "(" + pos.x.toFixed(2) + ", " + pos.y.toFixed(2) + ")";
		$("#hoverdata").text(str);
	
		if (item) {
			var x = item.datapoint[0],
				y = item.datapoint[1];
			
				$("#tooltip").html("Total Sales : " + y)
				.css({top: item.pageY+5, left: item.pageX+5})
				.fadeIn(200);
		} else {
			$("#tooltip").hide();
		}
	});

	
	
	
	
	plotWithOptions();
*/
	
	
	
	
	
	
	
	
	//Morris Chart (Total Visits)
$(function	()	{
	  var json_data = eval("("+series1+")");//(series1);
	  json_data=eval(json_data);
	  //alert(json_data);
	  //alert(json_data.length);
	  for (var i=0; i <json_data.length; i++){
		//alert(json_data[i]);  
	  }
	  data=json_data;
	  
	var totalVisitChart = new Morris.Bar({
	  element: 'totalSalesChart',
	  resize: true,
	  
	  data,
	  
/*	  
	  data: [
	    { y: '2018-5-21', a: 100, b: 90 },
	    { y: '2018-5-22', a: 75,  b: 65 },
	    { y: '2018-5-23', a: 50,  b: 80 },
	    { y: '2018-5-24', a: 75,  b: 65 },
	    { y: '2018-5-25', a: 50,  b: 40 },
	    { y: '2018-5-26', a: 75,  b: 65 },
	    { y: '2018-5-27', a: 100, b: 90 }
	  ],
	  */
	  xkey: 'time',
	  ykeys: ['sum_pro'],//'sum_acc'],// 'b'],
	  labels: ['机具销售额'],// '配件销售额'],
	  barColors: ['#00a65a'],// '#f56954'],
	  grid: false,
	  gridTextColor: '#777',
	  
	 
	});
	
	var json_data2 = eval("("+series2+")");//(series1);
	  json_data2=eval(json_data2);
	  for (var i=0; i <json_data2.length; i++){
		//alert(json_data2[i]);  
	  }
	  
	  data=json_data2;
	var peopleFlowChart = new Morris.Line({
	  element: 'peopleFlowChart',
	  resize: true, 
	  data,
/*
	  data: [
	    { y: '2018-5-21', a: 56 },
	    { y: '2018-5-22', a: 75 },
	    { y: '2018-5-23', a: 50 },
	    { y: '2018-5-24', a: 75 },
	    { y: '2018-5-25', a: 50 },
	    { y: '2018-5-26', a: 75 },
	    { y: '2018-5-27', a: 100 }
	  ],
*/
	  xkey: 'time',
	  ykeys: ['wifi_3m_num'],
	  labels: ['人流量'],
	  //barColors: ['#00a65a', '#f56954'],
	  grid: false,
	  gridTextColor: '#777',
	  
	 
	});
	
	var json_data3 = eval("("+series3+")");//(series1);
	  json_data3=eval(json_data3);
	  for (var i=0; i <json_data3.length; i++){
		//alert(json_data3[i]);  
	  }
	  data=json_data3;

	var customChart = new Morris.Bar({
	  element: 'customChart',
	  resize: true, 
	  data,
/*
	  data: [
	       { y: '2018-5-21', a: 56  },
	    { y: '2018-5-22', a: 75 },
	    { y: '2018-5-23', a: 50 },
	    { y: '2018-5-24', a: 75 },
	    { y: '2018-5-25', a: 50 },
	    { y: '2018-5-26', a: 75 },
	    { y: '2018-5-27', a: 100 }
	  ],
*/
	  xkey: 'time',
	  ykeys: ['wifi_1m_num'],
	  labels: ['有效客户'],
	  barColors: ['#00a65a', '#f56954'],
	  grid: false,
	  gridTextColor: '#777',
	  
	 
	});
	
	var json_data4 = eval("("+series4+")");//(series1);
	  json_data4=eval(json_data4);
	  for (var i=0; i <json_data4.length; i++){
		//alert(json_data4[i]);  
	  }
	data=json_data4;
	
	var chengjiaoChart = new Morris.Line({
	  element: 'chengjiao',
	  resize: true, 
	  data,
/*
	  data: [
	    { y: '2018-5-21', a: 56  },
	    { y: '2018-5-22', a: 75 },
	    { y: '2018-5-23', a: 50 },
	    { y: '2018-5-24', a: 75 },
	    { y: '2018-5-25', a: 50 },
	    { y: '2018-5-26', a: 75 },
	    { y: '2018-5-27', a: 100 }
	  ],
*/
	  xkey: 'time',
	  ykeys: ['quantity_pro'],//'quantity_acc'],
	  labels: ['机具成交量'],//'配件成交量'],
	  //barColors: ['#00a65a'],
	  grid: false,
	  gridTextColor: '#777',
	  
	 
	});
	
	var json_data5 = eval("("+series5+")");//(series1);
	  json_data5=eval(json_data5);
	  for (var i=0; i <json_data5.length; i++){
		//alert(json_data5[i]);  
	  }
	data=json_data5;
	
	var manyiduChart = new Morris.Bar({
	  element: 'manyidu',
	  resize: true, 
	  data,
/*
	  data: [
	    { y: '2018-5-21', a: 54, b: 2 , c:0},
	    { y: '2018-5-22', a: 75,  b: 3 , c:2},
	    { y: '2018-5-23', a: 50,  b: 5 , c:1},
	    { y: '2018-5-24', a: 75,  b: 1 , c:0 },
	    { y: '2018-5-25', a: 50,  b: 3 , c:3},
	    { y: '2018-5-26', a: 75,  b: 5 , c:2},
	    { y: '2018-5-27', a: 100, b: 6 , c:0}
	  ],
*/
	  xkey: 'time',
	  ykeys: ['excellent_num','good_num','unsatisfy_num'],
	  labels: ['非常满意', '满意', '不满意'],
	  barColors: ['#00a65a', '#CDAD00', '#ff0000'],
	  grid: false,
	  gridTextColor: '#777',
	  
	 
	});
	
	
	
	//Datepicker
	$('#calendar').DatePicker({
		flat: true,
		date: '2014-06-07',
		current: '2014-06-07',
		calendars: 1,
		starts: 1
	});

	//Skycon
	var icons = new Skycons({"color": "white"});
    icons.set("skycon1", "sleet");
    icons.set("skycon2", "partly-cloudy-day");
    icons.set("skycon3", "wind");
    icons.set("skycon4", "clear-day");
    icons.play();

	//Scrollable Chat Widget
	$('#chatScroll').slimScroll({
		height:'230px'
	});

	//Chat notification
	setTimeout(function() {
		$('.chat-notification').find('.badge').addClass('active');
		$('.chat-alert').addClass('active');
	}, 3000);

	setTimeout(function() {
		$('.chat-alert').removeClass('active');
	}, 8000);
	
	$(window).resize(function(e)	{
		// Redraw All Chart
		setTimeout(function() {
			totalVisitChart.redraw();
			peopleFlowChart.redraw();
			customChart.redraw();
			chengjiaoChart.redraw();
			manyiduChart.redraw();
			//plotWithOptions();
		},500);
	});

	$('#sidebarToggleLG').click(function()	{
		// Redraw All Chart
		setTimeout(function() {
			totalVisitChart.redraw();
			peopleFlowChart.redraw();
			customChart.redraw();
			chengjiaoChart.redraw();
			manyiduChart.redraw();
			//plotWithOptions();
		},500);
	});

	$('#sidebarToggleSM').click(function()	{
		// Redraw All Chart
		setTimeout(function() {
			totalVisitChart.redraw();
			peopleFlowChart.redraw();
			customChart.redraw();
			chengjiaoChart.redraw();
			manyiduChart.redraw();
			//plotWithOptions();
		},500);
	});
});


$(function	people()	{
$("#peopleFlowChart").tab("show",function(){
	var peopleFlowChart = new Morris.Line({
	  element: 'peopleFlowChart',
	  resize: true, 
	  data: [
	    { y: '2018-5-21', a: 56 },
	    { y: '2018-5-22', a: 75 },
	    { y: '2018-5-23', a: 50 },
	    { y: '2018-5-24', a: 75 },
	    { y: '2018-5-25', a: 50 },
	    { y: '2018-5-26', a: 75 },
	    { y: '2018-5-27', a: 100 }
	  ],
	  xkey: 'y',
	  ykeys: ['a'],
	  labels: ['1米范围'],
	  //barColors: ['#00a65a', '#f56954'],
	  grid: false,
	  gridTextColor: '#777',
	  
	 
	});
});
});
	
