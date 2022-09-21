google.charts.load('current', {'packages':['line']});
google.charts.setOnLoadCallback(drawChart);

var timer = [];
//P4
var robot = [];
var fisa2 = [];
var fisa4 = [];


//P5
var L13 = [];
var L14 = [];
var L15S1 = [];
var L15S2 = [];
var fisa3 = [];


//P9
var HC4 = [];
var HC5S1 = [];
var HC5S2 = [];
var AI = [];
var HC3 = [];
var HC6 = [];



function drawChart() {

    var optionsLP4 = {
        chart: {
          title: 'Phase4',
        },
        width: 900,
        height: 500
    };

    var optionsLP5 = {
      chart: {
        title: 'Phase5',
      },
      width: 900,
      height: 500
    };

    var optionsLP9 = {
      chart: {
        title: 'Phase9',
      },
      width: 900,
      height: 500
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
        robot.push(json[0].Data[0].Water);
        fisa2.push(json[0].Data[1].Water);
        fisa4.push(json[0].Data[2].Water);


        //P5
        L15S1.push(json[1].Data[0].Water);
        L15S2.push(json[1].Data[1].Water);
        fisa3.push(json[1].Data[2].Water);
        L13.push(json[1].Data[3].Water);
        L14.push(json[1].Data[4].Water);


        //P9
        HC4.push(json[2].Data[0].Water);
        HC5S1.push(json[2].Data[1].Water);
        HC5S2.push(json[2].Data[2].Water);
        AI.push(json[2].Data[3].Water);
        HC3.push(json[2].Data[4].Water);
        HC4.push(json[2].Data[5].Water);


         if (timer.length == 11) {
            timer.shift();
            robot.shift();
            fisa2.shift();
            fisa4.shift();
            L15S1.shift();
            L15S2.shift();
            fisa3.shift();
            L13.shift();
            L14.shift();
            HC4.shift();
            HC5S1.shift();
            HC5S2.shift();
            AI.shift();
            HC3.shift();
            HC4.shift();


         };

        var dataLP4 = new google.visualization.DataTable();
        dataLP4.addColumn('string', 'Time');
        dataLP4.addColumn('number', json[0].Data[0].id);
        dataLP4.addColumn('number', json[0].Data[1].id);
        dataLP4.addColumn('number', json[0].Data[2].id);


        for(i = 0; i < timer.length; i++){

          dataLP4.addRow([timer[i], robot[i], fisa2[i], fisa4[i]]);

        };
        
        var dataLP5 = new google.visualization.DataTable();
        dataLP5.addColumn('string', 'Time');
        dataLP5.addColumn('number', json[1].Data[0].id);
        dataLP5.addColumn('number', json[1].Data[1].id);
        dataLP5.addColumn('number', json[1].Data[2].id);
        dataLP5.addColumn('number', json[1].Data[3].id);
        dataLP5.addColumn('number', json[1].Data[4].id);


        for(i = 0; i < timer.length; i++){

          dataLP5.addRow([timer[i], L15S1[i], L15S2[i], fisa3[i], L13[i], L14[i]]);

        };

        var dataLP9 = new google.visualization.DataTable();
        dataLP9.addColumn('string', 'Time');
        dataLP9.addColumn('number', json[2].Data[0].id);
        dataLP9.addColumn('number', json[2].Data[1].id);
        dataLP9.addColumn('number', json[2].Data[2].id);
        dataLP9.addColumn('number', json[2].Data[3].id);
        dataLP9.addColumn('number', json[2].Data[4].id);
        dataLP9.addColumn('number', json[2].Data[5].id);

        
        for(i = 0; i < timer.length; i++){

          dataLP9.addRow([timer[i], HC4[i], HC5S1[i], HC5S2[i], AI[i], HC3[i], HC4[i]]);

        };

        chartLP4.draw(dataLP4, google.charts.Line.convertOptions(optionsLP4));
        chartLP5.draw(dataLP5, google.charts.Line.convertOptions(optionsLP5));
        chartLP9.draw(dataLP9, google.charts.Line.convertOptions(optionsLP9));
        }); 
    }
    //setInterval(drawLine, 1000);

var chartLP4 = new google.charts.Line(document.getElementById('linechartP4'));
var chartLP5 = new google.charts.Line(document.getElementById('linechartP5'));
var chartLP9 = new google.charts.Line(document.getElementById('linechartP9'));
}





