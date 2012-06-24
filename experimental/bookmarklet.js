if (!($ = window.jQuery)) { // typeof jQuery=='undefined' works too
    script = document.createElement( 'script' );
    script.src = 'http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js';
    script.onload=releasetheKraken;
    document.body.appendChild(script);
}

grabYouTubeId();

function grabYouTubeId() {
    // if on a YouTube page, this will grab the YouTube id
    var url = location.href.replace(/https?:\/\//i, "");
    var pattern = /(http:\/\/)?(?:www\.)?youtube.com\/watch\?(?=.*v=[\-\w]+)(?:\S+)?$/;
    if(pattern.test(url))
        var id = $('input[name="video_id"]').val();
}