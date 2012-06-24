javascript:void((function() {
	var grabYouTubeId = function() {
		// If on a YouTube page, this will grab the YouTube ID.
		var url = location.href.replace(/https?:\/\//i, "");
		var pattern = /(http:\/\/)?(?:www\.)?youtube.com\/watch\?(?=.*v=[\-\w]+)(?:\S+)?$/;
		var id;
		if (pattern.test(url)) {
			id = $('input[name="video_id"]').val();
		}
		return id;
	};

	var displayModalWindow = function() {
		var ytId = grabYouTubeId(); alert("Found ID: " + ytId);
	};

	if (!($ = window.jQuery)) { // typeof jQuery=='undefined' works too
		script = document.createElement('script');
		script.src = 'http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js';
		script.onload=displayModalWindow;
		document.body.appendChild(script);
	} else {
		displayModalWindow();
	}
})());
