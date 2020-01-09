var inputNumber = $('#externalVideoNumber');
var inputUrl = $('#externalVideoUrl');
var inputSubId = $('#sub_input_id');

$('.update-btn').click(function () {
    var videosubId = $(this).attr('data-id');
    var videosubUrl = $(this).attr('data-url');
    var videosubNumber = parseInt($(this).attr('data-number'));

    inputNumber.val(videosubNumber);
    inputUrl.val(videosubUrl);
    inputSubId.val(videosubId);
});