$(function() {
    $("#main-form").submit(function(ev) {
        var form = this;
    
        var allOk = validate(form, null);
    
        if (! allOk) {
            $("#error-modal").modal("show");
            ev.preventDefault();
        }
    });

    $(".question").click(function(item) {
        var name = $(this).attr("name");
        validate(this.form, [name]);
    });
});


function validate(form, questions) {
    // First get all the questions.
    if (! questions) {
        questions = [];
        $(".question-yes").each(function(i, input) {
            questions.push($(input).attr("name"));
        });
    }

    var allOk = true;
    $.each(questions, function(i, question) {
        console.log(question);
        var selector = "[name='" + question + "']:checked";
        var value = $(form).find(selector).val();

        var $error = $("#error-" + question);
        var $label = $("#label-" + question);
        if (! value) {
            allOk = false;
            $error.removeClass("hide");
            $label.addClass("error");
        } else {
            $error.addClass("hide");
            $label.removeClass("error");
        }
    });

    return allOk;
}
