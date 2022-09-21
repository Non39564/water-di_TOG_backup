google.charts.load('current', {'packages':['corechart', 'line']});
google.charts.setOnLoadCallback(drawLineChart);

var timer = [];
var idP4 = [];


$.getJSON('/dataapi', function (json) {
  //P4
  for (i in json[0].Data ){
    window[json[0].Data[i].id.replace(/ +/g, "")] = [];
  }
  //P5
  for (i in json[1].Data ){
    window[json[1].Data[i].id.replace(/ +/g, "")] = [];
  }
  //P9
  for (i in json[2].Data ){
    window[json[2].Data[i].id.replace(/ +/g, "").replace(/-/g, "")] = [];
  }
})

function drawLineChart() {

  var options = {
    'width':500,
    'height':500
  }

    var optionsLP4 = {
      isStacked: true,
        chart: {
          title: 'Phase4',
        },
        series: {
          1: {
            areaOpacity: 0.6,
            color: '#EF9A9A',
            visibleInLegend: false,
            type: 'area'
          },
          2: {
            areaOpacity: 0.6,
            color: '#fee000',
            visibleInLegend: false,
            type: 'area'},
          3: {
            areaOpacity: 0.6,
            color: '#9ff78d',
            visibleInLegend: false,
            type: 'area'},
        },
    };

    var optionsLP5 = {
      isStacked: true,
      chart: {
        title: 'Phase5',
      },
      series: {
        1: {
          areaOpacity: 0.6,
          color: '#EF9A9A',
          visibleInLegend: false,
          type: 'area'
        },
        2: {
          areaOpacity: 0.6,
          color: '#fee000',
          visibleInLegend: false,
          type: 'area'},
        3: {
          areaOpacity: 0.6,
          color: '#9ff78d',
          visibleInLegend: false,
          type: 'area'},
      },
    };

    var optionsLP9 = {
      isStacked: true,
      chart: {
        title: 'Phase9',
      },
      series: {
        0: {
          areaOpacity: 0.6,
          color: '#EF9A9A',
          visibleInLegend: false,
          type: 'area'
        },
        1: {
          areaOpacity: 0.6,
          color: '#fee000',
          visibleInLegend: false,
          type: 'area'},
        2: {
          areaOpacity: 0.6,
          color: '#9ff78d',
          visibleInLegend: false,
          type: 'area'},
      },
    };

      function drawLine() {
        $.getJSON('/dataapi', function (json) {
        function addLeadingZero(num) {
            return (num <= 9) ? ("0" + num) : num;
          }
    
        currDate = new Date(),
        time = addLeadingZero(currDate.getHours()) + ":" +
        addLeadingZero(currDate.getMinutes()) + ":" +
        addLeadingZero(currDate.getSeconds());
        
        timer.push(time.toString());
        //P4
        for (i in json[0].Data){
          window[json[0].Data[i].id.replace(/ +/g, "")].push(json[0].Data[i].Water);
        }
        //P5
        for (i in json[1].Data){
          window[json[1].Data[i].id.replace(/ +/g, "")].push(json[1].Data[i].Water);
        }
        //P9
        for (i in json[2].Data){
          window[json[2].Data[i].id.replace(/ +/g, "").replace(/-/g, '')].push(json[2].Data[i].Water);
        }
        if (timer.length == 11) {
           timer.shift();
           //P4
           for (i in json[0].Data ){
             window[json[0].Data[i].id.replace(/ +/g, "")].shift();
           }
           //P5
           for (i in json[1].Data ){
             window[json[1].Data[i].id.replace(/ +/g, "")].shift();
           }
           //P9
           for (i in json[2].Data ){
             window[json[2].Data[i].id.replace(/ +/g, "").replace(/-/g, '')].shift();
           }
        };

        var dataLP4 = new google.visualization.DataTable();
        dataLP4.addColumn('string', 'Time');
        for (i in json[0].Data){
          dataLP4.addColumn('number', json[0].Data[i].id);
          idP4.push(json[0].Data[i].id)
        }
        dataLP4.addColumn('number', 'Low');
        dataLP4.addColumn('number', 'Monitor');
        dataLP4.addColumn('number', 'Normal');
        for (i = 0; i < timer.length; i++){
          dataLP4.addRow([timer[i], ROBOT[i], 10, 3, 17]);//, Fisa2[i], Fisa4[i]
        };
        
        var dataLP5 = new google.visualization.DataTable();
        dataLP5.addColumn('string', 'Time');
        for (i in json[1].Data){
          dataLP5.addColumn('number', json[1].Data[i].id);
        }
        for(i = 0; i < timer.length; i++){
          dataLP5.addRow([timer[i]]);//, L15Station1[i], L15Station2[i], Fisa3[i], L13[i], L14[i]
        };

        var dataLP9 = new google.visualization.DataTable();
        dataLP9.addColumn('string', 'Time');
        dataLP9.addColumn('number', 'Low');
        dataLP9.addColumn('number', 'Monitor');
        dataLP9.addColumn('number', 'Normal');
        for (i in json[2].Data){
          dataLP9.addColumn('number', json[2].Data[i].id);
        }
        for(i = 0; i < timer.length; i++){
          dataLP9.addRow([timer[i], 10, 3, 17, HC4[i], HC3[i], HC6[i], HC5Station1[i], HC5Station2[i]]);//,AI[i]
        };

        chartLP4.draw(dataLP4, optionsLP4);
        if (dataLP5.getNumberOfColumns() === 1){
          $( "#dataP5" ).text( "No data available" );
        } else {
          chartLP5.draw(dataLP5, optionsLP5);
        }
        chartLP9.draw(dataLP9, 
          optionsLP9);
        }); 
    }
    setInterval(drawLine, 1000);

var chartLP4 = new google.visualization.ComboChart(document.getElementById('linechartP4'));
var chartLP5 = new google.visualization.ComboChart(document.getElementById('linechartP5'));
var chartLP9 = new google.visualization.ComboChart(document.getElementById('linechartP9'));
}

$(window).resize(function(){
  drawLineChart();
});