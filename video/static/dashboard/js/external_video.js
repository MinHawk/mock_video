
var videoAreaStatus = false;
var videoEditArea = $('#video-edit-area');

$('#show_video_create_btn').click(function () {
    if (!videoAreaStatus) {
        videoEditArea.show();
        videoAreaStatus = true;
    } else {
        videoEditArea.hide();
        videoAreaStatus = false
    }
})