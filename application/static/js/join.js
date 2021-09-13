  $(function () {
    $("#wizard").steps({
      headerTag: "h4",
      bodyTag: "section",
      transitionEffect: "fade",
      enableAllSteps: true,
      transitionEffectSpeed: 500,
      onStepChanging: function (event, currentIndex, newIndex) {
        if (newIndex === 1) {
          $('.steps ul').addClass('step-2');
        } else {
          $('.steps ul').removeClass('step-2');
        }
        if (newIndex === 2) {
          $('.steps ul').addClass('step-3');
          $('.actions ul').addClass('step-last');
        } else {
          $('.steps ul').removeClass('step-3');
          $('.actions ul').addClass('step-last');
        }
        return true;
      },
      labels: {
        finish: "Order again",
        next: "Next",
        previous: "Previous"
      }
    });
    // Custom Steps Jquery Steps
    $('.wizard > .steps li a').click(function () {
      $(this).parent().addClass('checked');
      $(this).parent().prevAll().addClass('checked');
      $(this).parent().nextAll().removeClass('checked');
    });
    // Custom Button Jquery Steps
    $('.forward').click(function () {
      $("#wizard").steps('next');
    })
    $('.backward').click(function () {
      $("#wizard").steps('previous');
    })
    // Checkbox
    $('.checkbox-circle label').click(function () {
      $('.checkbox-circle label').removeClass('active');
      $(this).addClass('active');
    })
  })

  $(function () {
    $("#wizard_login").steps({
      headerTag: "h4",
      bodyTag: "section",
      transitionEffect: "fade",
      enableAllSteps: true,
      transitionEffectSpeed: 500,
      onStepChanging: function (event, currentIndex, newIndex) {
        if (newIndex === 1) {
          $('.steps ul').addClass('step-2');
        } else {
          $('.steps ul').removeClass('step-2');
        }
        if (newIndex === 2) {
          $('.steps ul').addClass('step-3');
          $('.actions ul').addClass('step-last');
        } else {
          $('.steps ul').removeClass('step-3');
          $('.actions ul').addClass('step-last');
        }
        return true;
      },
      labels: {
        finish: "Login",
      }
    });
    // Custom Steps Jquery Steps
    $('.wizard_login > .steps li a').click(function () {
      $(this).parent().addClass('checked');
      $(this).parent().prevAll().addClass('checked');
      $(this).parent().nextAll().removeClass('checked');
    });
    // Custom Button Jquery Steps
    $('.forward').click(function () {
      $("#wizard_login").steps('next');
    })
    $('.backward').click(function () {
      $("#wizard_login").steps('previous');
    })
    // Checkbox
    $('.checkbox-circle label').click(function () {
      $('.checkbox-circle label').removeClass('active');
      $(this).addClass('active');
    })
  })