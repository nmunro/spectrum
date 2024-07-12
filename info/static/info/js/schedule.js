$(function() {
  var date = new Date();
  var month = date.getMonth();
  var nth = ['1', '2', '3', '4', 'Last'];
  var rrule = {
    asString: "FREQ=YEARLY;BYMONTH=1;BYMONTHDAY=1",
    nth: nth,
    date: date,
    nthDay: nth[Math.floor(date.getDate()/7)],
    year: date.getFullYear(),
    month: month,
    humanMonth: month + 1,
    monthday: date.getDate(),
    day: date.getDay(),
    days: ['SU', 'MO', 'TU', 'WE', 'TH', 'FR', 'SA'],
    monthdays: [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31],
    updateRrule: function(ruleType) {
      var end = '';
      if($('#rrules-end .count:visible').length > 0) {
          var interval = Math.round($('#rrules-end .interval').val());
          if(!Number.isInteger(interval) || interval < 1) {
            interval = 1;
          }
        end = ';COUNT=' + interval;
      }
      if($('#rrules-end .until:visible').length > 0) {
        var date = new Date($('#rrules-end .date').val());
        if(!(date.toString() === 'Invalid Date')) {
          var month = '' + (date.getMonth() + 1);
          var day = '' + date.getDate();
          var year = date.getFullYear();
          if (month.length < 2) month = '0' + month;
          if (day.length < 2) day = '0' + day;
          end = ';COUNT=' + year + month + day;
        }
      }
      switch(ruleType) {
        case 'yearly-on': {
          var month = $('#rrule .yearly .yearly-on .month').val();
          var monthday = $('#rrule .yearly .yearly-on .monthday').val();
          rrule.asString = "FREQ=YEARLY;BYMONTH=" + month + ";BYMONTHDAY=" + monthday + end;
          break;
        }
        case 'yearly-onthe': {
          var month = $('#rrule .yearly .yearly-onthe .month').val();
          var day = $('#rrule .yearly .yearly-onthe .day').val();
          var nth = $('#rrule .yearly .yearly-onthe .nth').val();
          rrule.asString = "FREQ=YEARLY;BYMONTH=" + month + ";BYDAY=" + day + ";BYSETPOS=" + nth + end;
          break;
        }
        case 'monthly-on': {
          var monthday = $('#rrule .monthly .monthly-on .monthday').val();
          var interval = Math.round($('#rrule .monthly .interval').val());
          if(!Number.isInteger(interval) || interval < 1) {
            interval = 1;
          }
          rrule.asString = "FREQ=MONTHLY;BYMONTHDAY=" + monthday + ";INTERVAL=" + interval + end;
          break;
        }
        case 'monthly-onthe': {
          var interval = Math.round($('#rrule .monthly .interval').val());
          if(!Number.isInteger(interval) || interval < 1) {
            interval = 1;
          }
          var day = $('#rrule .monthly .monthly-onthe .day').val();
          var nth = $('#rrule .monthly .monthly-onthe .nth').val();
          rrule.asString = "FREQ=MONTHLY;INTERVAL=" + interval + ";BYDAY=" + day + ";BYSETPOS=" + nth + end;
          break;
        }
        case 'weekly': {
          var interval = Math.round($('#rrule .weekly .interval').val());
          if(!Number.isInteger(interval) || interval < 1) {
            interval = 1;
          }
          var days = "";
          $('#rrule .weekly input[type="checkbox"]:checked').each(function(index){
            if(this.checked) {
              if(index > 0) {
                days += ',';
              }
              days += this.value;
            }
          });
          if(days.length == 0) {
            days = rrule.days[rrule.day];
          }
          rrule.asString = "FREQ=WEEKLY;INTERVAL=" + interval + ";BYDAY=" + days + end;
          break;
        }
        case 'daily': {
          var interval = Math.round($('#rrule .daily .interval').val());
          if(!Number.isInteger(interval) || interval < 1) {
            interval = 1;
          }
          rrule.asString = "FREQ=DAILY;INTERVAL=" + interval + end;
          break;
        }
        default: {
          rrule.asString = "";
          break;
        }
      }
      $('#rrule').data('rrule', rrule.asString);
      $('#result').html($('#rrule').data('rrule'));
    }
  };
  $(function() {
    $('#rrule .day').each(function(){
      $(this).val(rrule.days[rrule.day]);
    });
    $('#rrule .days').each(function(){
      var selector = 'input[value="' + rrule.days[rrule.day] + '"]';
      $(this).find(selector).prop('checked', true);
    })
    $('#rrule .monthly-on .monthday').each(function(){
      var $monthday = $(this);
      $monthday.val(rrule.monthday);
      $monthday.trigger('change');
    });
    $('#rrule .monthly-on select').on('change', function(){
      rrule.updateRrule('monthly-on');
    });
    $('#rrule .monthly-onthe select').on('change', function(){
      rrule.updateRrule('monthly-onthe');
    });
    $('#rrule .frequency').on('change', function(){
      var selected = $(this).val().toLowerCase();
      $('#rrule').children().each(function(){
        var $this = $(this);
        if($this.hasClass(selected) || this.hasAttribute('id')) {
          $this.css('display', 'block');
        }
        else {
          $this.css('display', 'none');
        }
        if($this.hasClass(selected)) {
          if(this.hasAttribute('data-selector')) {
            rrule.updateRrule($this.data('selector'));
          }
          else {
            rrule.updateRrule($this.find('*[data-selector]:visible').data('selector'));
          }
        }
      });
    });
    $('#rrule .monthly .interval, #rrule .daily .interval').on('change input', function(){
      rrule.updateRrule($('#rrule *[data-selector]:visible').data('selector'));
    });
    $('#rrule .weekly input').on('change input', function(){
      rrule.updateRrule('weekly');
    });
    $('#rrule .monthly .type').on('change', function(){
      var $this = $(this);
      if($this.val() == 'on') {
        $('#rrule .monthly .monthly-on').css('display', 'inline');
        $('#rrule .monthly .monthly-onthe').css('display', 'none');
        rrule.updateRrule('monthly-on');
      }
      else {
        $('#rrule .monthly .monthly-on').css('display', 'none');
        $('#rrule .monthly .monthly-onthe').css('display', 'inline');
        rrule.updateRrule('monthly-onthe');
      }
    });
    $('#rrule .yearly .type').on('change', function(){
      var $this = $(this);
      if($this.val() == 'on') {
        $('#rrule .yearly .yearly-on').css('display', 'inline');
        $('#rrule .yearly .yearly-onthe').css('display', 'none');
        rrule.updateRrule('yearly-on');
      }
      else {
        $('#rrule .yearly .yearly-on').css('display', 'none');
        $('#rrule .yearly .yearly-onthe').css('display', 'inline');
        rrule.updateRrule('yearly-onthe');
      }
    });
    $('#rrule .yearly .yearly-onthe select').on('change', function(){
      rrule.updateRrule('yearly-onthe');
    });
    $('#rrule .yearly .yearly-on .monthday').on('change', function(){
      rrule.updateRrule('yearly-on');
    });
    $('#rrule .yearly .yearly-on .month').on('change', function(){
      var $this = $(this);
      var selectedMonth = $this.val() - 1;
      var days = rrule.monthdays[selectedMonth];
      var $monthday = $this.next();
      $monthday.html("");
      for(var i=1;i<=days;i++) {
        var $option = $("<option value='" + i + "'>" + i + "</option>");
        $option.appendTo($monthday);
      }
      if(selectedMonth == month) {
        $monthday.val(rrule.monthday);
        $monthday.trigger('change');
      }
      else {
        $monthday.val(1);
        $monthday.trigger('change');
      }
    }).val(rrule.humanMonth).trigger('change');
    $('#rrules-end span input').on('change, input', function(){
      rrule.updateRrule($('#rrule *[data-selector]:visible').data('selector'));
    });
    $('#rrules-end .ends').on('change', function(){
      $('#rrules-end > span').css('display', 'none');
      switch($(this).val()) {
        case 'count': {
          $('#rrules-end .count').css('display', 'inline');
          break;
        }
        case 'until': {
          $('#rrules-end .until').css('display', 'inline');
          break;
        }
        default: {
          break;
        }
      }
      rrule.updateRrule($('#rrule *[data-selector]:visible').data('selector'));
    });
    var tomorrow = new Date();
    tomorrow.setDate(tomorrow.getDate()+1);
    $('#rrules-end .date').on('changeDate', function(){
      $(this).datepicker('hide');
      rrule.updateRrule($('#rrule *[data-selector]:visible').data('selector'));
    }).datepicker('update', tomorrow).datepicker('setStartDate', tomorrow);
    $.fn.datepicker.defaults.format = "mm/dd/yyyy";
  });
})
