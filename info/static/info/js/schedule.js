$(function() {
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

    $("#yearly-type").change(function() {
      const type = $(this).val();
      const parent = $(this).closest('div');

      parent.find('[data-selector]').hide();
      parent.find(`[data-selector=${type}]`).show();

      if ($(this).val() === "on") {
        $(".yearly-on").show();
        $(".yearly-onthe").hide();
      } else if ($(this).val() === "onthe") {
        $(".yearly-on").hide();
        $(".yearly-onthe").show();
      }
    }).trigger("change");

    $("#monthly-type").change(function() {
      const type = $(this).val();
      const parent = $(this).closest('div');

      parent.find('[data-selector]').hide();
      parent.find(`[data-selector=${type}]`).show();

      if ($(this).val() === "on") {
        $(".monthly-on").show();
        $(".monthly-onthe").hide();
        console.log("on");
      } else if ($(this).val() === "onthe") {
        $(".monthly-on").hide();
        $(".monthly-onthe").show();
      }
    }).trigger("change");


    // Show/hide options for yearly and monthly types
    // $('#yearly-type, #monthly-type').change(function() {
    //     const type = $(this).val();
    //     const parent = $(this).closest('div');

    //     if ($(this).val() === "on") {
    //       $("#yearly-on").show();
    //       $("#yearly-onthe").hide();
    //       console.log("on");
    //     } else if ($(this).val() === "onthe") {
    //       $("#yearly-on").hide();
    //       $("#yearly-onthe").show();
    //       console.log("onthe");
    //     }

    //     // parent.find('[data-selector]').hide();
    //     // parent.find(`[data-selector=${type}]`).show();
    // }).trigger('change');

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
});
