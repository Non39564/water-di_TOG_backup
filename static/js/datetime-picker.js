if (/Mobi/.test(navigator.userAgent)) {
    // if mobile device, use native pickers
    $(".date input").attr("type", "date");
    $(".time input").attr("type", "time");
  } else {
    // if desktop device, use DateTimePicker
    $("#date_now").datetimepicker({
      useCurrent: false,
      format: "YYYY-MM-DD",
      showTodayButton: true,
      icons: {
        next: "fa fa-chevron-right",
        previous: "fa fa-chevron-left",
        today: 'todayText',
      }
    });
    $("#date_range_finish").datetimepicker({
      useCurrent: false,
      format: "YYYY-MM-DD",
      showTodayButton: true,
      icons: {
        next: "fa fa-chevron-right",
        previous: "fa fa-chevron-left",
        today: 'todayText',
      }
    });
    $("#date_it_finish").datetimepicker({
      useCurrent: false,
      format: "YYYY-MM-DD",
      showTodayButton: true,
      icons: {
        next: "fa fa-chevron-right",
        previous: "fa fa-chevron-left",
        today: 'todayText',
      }
    });
    $("#date_it_deliver").datetimepicker({
      useCurrent: false,
      format: "YYYY-MM-DD",
      showTodayButton: true,
      icons: {
        next: "fa fa-chevron-right",
        previous: "fa fa-chevron-left",
        today: 'todayText',
      }
    });
    $("#date_it_getWork").datetimepicker({
      useCurrent: false,
      format: "YYYY-MM-DD",
      showTodayButton: true,
      icons: {
        next: "fa fa-chevron-right",
        previous: "fa fa-chevron-left",
        today: 'todayText',
      }
    });
    $("#date_it_now").datetimepicker({
      useCurrent: false,
      format: "YYYY-MM-DD",
      showTodayButton: true,
      icons: {
        next: "fa fa-chevron-right",
        previous: "fa fa-chevron-left",
        today: 'todayText',
      }
    });
    
    $("#time_now").datetimepicker({
      format: "LT",
      icons: {
        up: "fa fa-chevron-up",
        down: "fa fa-chevron-down"
      }
    });
  }