$(function() {
  const init = $("#rrule-output").val() === "";
  const rruleOutput = $("#rrule-output").val();

  // Populate day dropdowns
  for (let i = 1; i <= 31; i++) {
    $('.monthday').append(`<option value="${i}">${i}</option>`);
  }

  // Show/hide sections based on frequency
  $('#frequency').change(function() {
      const freq = $(this).val();
      $('.yearly, .monthly, .weekly, .daily').hide();
      $(`.${freq.toLowerCase()}`).show();
  }).trigger('change');

  // Change handlers for yearly and monthly types
  $("#yearly-type").change(function() {
    const type = $(this).val();
    const parent = $(this).closest('div');

    parent.find('[data-selector]').hide();
    parent.find(`[data-selector=yearly-${type}]`).show();
  }).trigger("change");

  $("#monthly-type").change(function() {
    const type = $(this).val();
    const parent = $(this).closest('div');

    parent.find('[data-selector]').hide();
    parent.find(`[data-selector=monthly-${type}]`).show();
  }).trigger("change");

  // Show/hide end options
  $('#ends').change(function() {
      const end = $(this).val();
      $('.count, .until').hide();
      if (end === 'count') {
          $('.count').show();
      } else if (end === 'until') {
          $('.until').show();
      }
  }).trigger('change');

  // Generate RRULE
  $('form').on('change', function() {
    const freq = $('#frequency').val();
    let rrule = `FREQ=${freq}`;

    if (freq === 'YEARLY') {
      const type = $('#yearly-type').val();
      if (type === 'on') {
        const month = $('#yearly-month').val();
        const monthday = $('#yearly-monthday').val();
        rrule += `;BYMONTH=${month};BYMONTHDAY=${monthday}`;
      } else {
        const nth = $('#yearly-nth').val();
        const day = $('#yearly-day').val();
        const month = $('#yearly-onthe-month').val();
        rrule += `;BYSETPOS=${nth};BYDAY=${day};BYMONTH=${month}`;
      }
    } else if (freq === 'MONTHLY') {
      const interval = $('#monthly-interval').val();
      rrule += `;INTERVAL=${interval}`;
      const type = $('#monthly-type').val();
      if (type === 'on') {
        const monthday = $('#monthly-monthday').val();
        rrule += `;BYMONTHDAY=${monthday}`;
      } else {
        const nth = $('#monthly-nth').val();
        const day = $('#monthly-day').val();
        rrule += `;BYSETPOS=${nth};BYDAY=${day}`;
      }
    } else if (freq === 'WEEKLY') {
      const interval = $('#weekly-interval').val();
      rrule += `;INTERVAL=${interval}`;
      const days = $('.weekly input:checked').map(function() {
        return $(this).val();
      }).get();
      if (days.length > 0) {
        rrule += `;BYDAY=${days.join(',')}`;
      }
    } else if (freq === 'DAILY') {
      const interval = $('#daily-interval').val();
      rrule += `;INTERVAL=${interval}`;
    }

    const ends = $('#ends').val();
    if (ends === 'count') {
      const count = $('#end-count').val();
      rrule += `;COUNT=${count}`;
    } else if (ends === 'until') {
      const until = $('#end-date').val();
      rrule += `;UNTIL=${until.replace(/-/g, '')}T000000Z`;
    }

    $('#rrule-output').val(rrule);
  }).trigger('change');

  if (!init) {
    const rRule = parseRRule(rruleOutput);

    $("#frequency").val(rRule.freq).trigger("change");

    if (rRule.freq === "YEARLY") {
      if (rRule.bymonth && rRule.bymonthday) {
        $("#yearly-type").val("on").trigger("change");
        $("#yearly-month").val(rRule.bymonth);
        $("#yearly-monthday").val(rRule.bymonthday);
      } else if (rRule.bysetpos && rRule.byday && rRule.bymonth) {
        $("#yearly-type").val("onthe").trigger("change");
        $("#yearly-nth").val(rRule.bysetpos);
        $("#yearly-day").val(rRule.byday);
        $("#yearly-onthe-month").val(rRule.bymonth);
      }
    } else if (rRule.freq === "MONTHLY") {
      $("#monthly-interval").val(rRule.interval).trigger("change");
      if (rRule.bymonthday) {
        $("#monthly-type").val("on").trigger("change");
        $("#monthly-monthday").val(rRule.bymonthday);
      } else if (rRule.bysetpos && rRule.byday) {
        $("#monthly-type").val("onthe").trigger("change");
        $("#monthly-nth").val(rRule.bysetpos);
        $("#monthly-day").val(rRule.byday);
      }
    } else if (rRule.freq === "WEEKLY") {
      $("#weekly-interval").val(rRule.interval);
      if (rRule.byday) {
        const days = rRule.byday.split(",");
        days.forEach(day => {
          $(`#weekly-${day.toLowerCase()}`).prop("checked", true);
        });
      }
    } else if (rRule.freq === "DAILY") {
      $("#daily-interval").val(rRule.interval);
    }

    if (rRule.count) {
      $("#ends").val("count").trigger("change");
      $("#end-count").val(rRule.count);
    } else if (rRule.until) {
      $("#ends").val("until").trigger("change");
      $("#end-date").val(rRule.until.substring(0, 8));
    } else {
      $("#ends").val("never").trigger("change");
    }
  }
});

function parseRRule(rrule) {
  const ruleObject = {};
  const rules = rrule.split(';');

  rules.forEach(rule => {
    const [key, value] = rule.split('=');
    if (key && value) {
      ruleObject[key.toLowerCase()] = value;
    }
  });

  return ruleObject;
}
