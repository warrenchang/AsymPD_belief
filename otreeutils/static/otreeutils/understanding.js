var N_QUESTIONS = null;
var QUIZ_ATTEMPTS = null;
var HINT_TEXT_EMPTY = null;
var wrong_attempts = 0;
var input_wrong_attempts = null;



// the following function is called whenever the server sends message after liveSend() is used
function liveRecv(data) {
    wrong_attempts = data;
    console.log('Inside liveRecv: received data:'+ data);
}


function checkUnderstandingQuestionsForm() {
    var n_correct = 0;

    // check whether each answer is correct
    for (var q_idx = 0; q_idx < N_QUESTIONS; q_idx++) {
        var input_id = 'id_q_input_' + q_idx;
        var input_field = $('#' + input_id);
        var label = $('label[for=' + input_id + ']');
        var v = input_field.val();
        var correct = $('#id_q_correct_' + q_idx).val();

        if (v == correct) {
            input_field.removeClass('error').addClass('ok');
            label.removeClass('error').addClass('ok');
            n_correct++;
        } else {
            input_field.removeClass('ok').addClass('error');
            label.removeClass('ok').addClass('error');

            var input_parent = input_field.parent();
            if (input_parent.find('.hint').length == 0) {
                var hint_text;
                if (v == '') {
                    hint_text = HINT_TEXT_EMPTY;
                } else {
                    hint_text = $('#id_q_hint_' + q_idx).val();
                }
                var hint = '<p class="hint">' + hint_text + '</p>';
                input_parent.append(hint);
            }
        }
    }

    // .val() is used to get/replace input elements values in jQuery, alternative in JS is .value.
    // innerHTML or jQuery's .html() is used to get/replace the whole markup inside an element, not input elements.
    // text() is used almost the same as JS innertHTML, only it gets/replaces the text inside an element,
    // not all the tags etc. It's bassically the equivalent of JS innerText
    if (n_correct == N_QUESTIONS) {
        input_wrong_attempts.val(wrong_attempts);
        $('#form').submit();
    } else {
        wrong_attempts += 1;
        liveSend(wrong_attempts);
        input_wrong_attempts.val(wrong_attempts);
        if (QUIZ_ATTEMPTS!=0){
            if (wrong_attempts>QUIZ_ATTEMPTS){
                $('#form').submit();
            }
            $('#attempts_used').html('You have used '+ wrong_attempts + ' out of ' + QUIZ_ATTEMPTS + ' attempts.' );
            console.log('print new value of wrong_attempts:' + wrong_attempts);
        }
    }
}


function setupUnderstandingQuestionsForm(n_questions, quiz_attempts, hint_text_empty, field_n_wrong_attempts, set_correct_answers) {
    N_QUESTIONS = n_questions;
    QUIZ_ATTEMPTS = quiz_attempts;
    HINT_TEXT_EMPTY = hint_text_empty;
    input_wrong_attempts = $('#id_' + field_n_wrong_attempts); // field in the form to be submitted

    liveSend('initialization');
    // $('#attempts_used').html('Test message: you have in total '+ QUIZ_ATTEMPTS + ' attempts.' );
    for (var q_idx = 0; q_idx < N_QUESTIONS; q_idx++) {
        var input_id = 'id_q_input_' + q_idx;
        var input_field = $('#' + input_id);
        var label = $('label[for=' + input_id + ']');

        if (set_correct_answers) {
            var correct = $('#id_q_correct_' + q_idx).val();
            input_field.val(correct);
        }

        input_field.focus(function (e) {   // reset classes function
            var inp = $(e.target);
            var par = inp.parent();
            var lbl = $('label[for=' + inp.prop('id') + ']');
            inp.removeClass('ok').removeClass('error');
            lbl.removeClass('ok').removeClass('error');
            par.find('.hint').remove();
        });
    }
}