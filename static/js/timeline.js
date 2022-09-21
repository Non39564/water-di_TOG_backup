const status = ["1", "2", "3", "4", null];
//let timeline = "";
for (let i = 0; i < status.length; i++) {
  timeline = status[4] ;
  if ($("#data").val() === "1"){
    $("#timeline-Received").removeClass("border-warning");
    $("#timeline-Received").addClass("border-gray");
    $("#date-Received").removeClass("bg-warning");
    $("#date-Received").addClass("bg-dark bg-opacity-25");
    $("#icon-Received").removeClass("text-warning");
    $("#icon-Received").addClass("text-dark text-opacity-25");
    $("#Received").addClass("text-dark text-opacity-50");
    $("#timeline-InProgress").removeClass("border-info");
    $("#timeline-InProgress").addClass("border-gray");
    $("#date-InProgress").removeClass("bg-info");
    $("#date-InProgress").addClass("bg-dark bg-opacity-25");
    $("#icon-InProgress").removeClass("text-info");
    $("#icon-InProgress").addClass("text-dark text-opacity-25");
    $("#InProgress").addClass("text-dark text-opacity-50");
    $("#timeline-Done").removeClass("border-success");
    $("#timeline-Done").addClass("border-gray");
    $("#date-Done").removeClass("bg-success");
    $("#date-Done").addClass("bg-dark bg-opacity-25");
    $("#icon-Done").removeClass("text-success");
    $("#icon-Done").addClass("text-dark text-opacity-25");
    $("#Done").addClass("text-dark text-opacity-50");
  } else if ($("#data").val() === "2") {
    $("#timeline-InProgress").removeClass("border-info");
    $("#timeline-InProgress").addClass("border-gray");
    $("#date-InProgress").removeClass("bg-info");
    $("#date-InProgress").addClass("bg-dark bg-opacity-25");
    $("#icon-InProgress").removeClass("text-info");
    $("#icon-InProgress").addClass("text-dark text-opacity-25");
    $("#InProgress").addClass("text-dark text-opacity-50");
    $("#timeline-Done").removeClass("border-success");
    $("#timeline-Done").addClass("border-gray");
    $("#date-Done").removeClass("bg-success");
    $("#date-Done").addClass("bg-dark bg-opacity-25");
    $("#icon-Done").removeClass("text-success");
    $("#icon-Done").addClass("text-dark text-opacity-25");
    $("#Done").addClass("text-dark text-opacity-50");
  } else if ($("#data").val() === "3") {
    $("#timeline-Done").removeClass("border-success");
    $("#timeline-Done").addClass("border-gray");
    $("#date-Done").removeClass("bg-success");
    $("#date-Done").addClass("bg-dark bg-opacity-25");
    $("#icon-Done").removeClass("text-success");
    $("#icon-Done").addClass("text-dark text-opacity-25");
    $("#Done").addClass("text-dark text-opacity-50");
  } else {
  }
}