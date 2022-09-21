google.charts.load('current', {'packages':['gauge']});
google.charts.setOnLoadCallback(drawChart);

var start = new Date().getTime();
var end = new Date().getTime();
var time = end - start;

function drawChart() {

  // $.getJSON('/dataapi').done(function (json){
  //   for (i in json){
  //     var id = (json[i].Phase).replace(/ +/g, "").replace(/-/g, '')
  //     var data = (json[i].Station+" "+json[i].Phase).replace(/ +/g, "").replace(/-/g, '')
  //     $('#card-body').prepend($(`<div class="p-1 mb-2 bg-dark bg-gradient text-white">
  //     <h2 class="text-center m-0" id="${id}"></h2>
  //     </div>
  //     <div id="${data}" class="display ${data} "></div>`));
  //     $(`#${id}`).text(json[i].Station+" "+json[i].Phase)
  //   }
  // })

  function drawGauge() {
    $.getJSON('/dataapi').done(function (json){

      var dataP4 = new google.visualization.DataTable();
      dataP4.addColumn('string', 'Label');
      dataP4.addColumn('number', 'Value');

      var dataP5 = new google.visualization.DataTable();
      dataP5.addColumn('string', 'Label');
      dataP5.addColumn('number', 'Value');

      var dataP9 = new google.visualization.DataTable();
      dataP9.addColumn('string', 'Label');
      dataP9.addColumn('number', 'Value');

      for (i in json){
        var id = (json[i].Phase).replace(/ +/g, "").replace(/-/g, '')
        $(`#${id}`).text(json[i].Station+" "+json[i].Phase)
      }

      for (i in json[0].Data) {
        dataP4.addRow([json[0].Data[i].id, json[0].Data[i].Water])
      }
 
      for (i in json[1].Data) {
        dataP5.addRow([json[1].Data[i].id, json[1].Data[i].Water]);
      }

      for (i in json[2].Data) {
        dataP9.addRow([json[2].Data[i].id, json[2].Data[i].Water]);
      }

          
      chartP4.draw(dataP4, options);
      chartP5.draw(dataP5, options);
      chartP9.draw(dataP9, options);

    });
  }


    var chartP4 = new google.visualization.Gauge(document.getElementById(`dataP4`));
    var chartP5 = new google.visualization.Gauge(document.getElementById(`dataP5`));
    var chartP9 = new google.visualization.Gauge(document.getElementById(`dataP9`));

  var options = {
    redFrom: 0, redTo: 12, redColor: "FF6609" ,
    yellowFrom: 12, yellowTo: 13, yellowColor: "FFE126",
    greenFrom: 13, greenTo: 30,greenColor: "1BFA00",
    min: 0, max: 30,
    minorTicks: 0,
  };

  setInterval(drawGauge, 1000);
}

$(window).resize(function(){
  drawChart();
});
