javascript:void((function() {
	var grabYouTubeIds = function() {
		var ids = new Array();

		/* If on a YouTube page, this will grab the primary YouTube ID. */
		var url = location.href.replace(/https?:\/\//i, '');
		var pattern = /(http:\/\/)?(?:www\.)?youtube.com\/watch\?(?=.*v=[\-\w]+)(?:\S+)?$/;
		if (pattern.test(url)) {
			var title = $('#eow-title').attr('title');
			var videoId = $('input[name="video_id"]').val();
			ids.push([title, videoId]);
		}

		/* Grab all related video IDs. */
		$('li.video-list-item > a.related-video').each(function(index, element) {
			var title = '';
			var children = element.childNodes;
			for (var i = 0; i < children.length; i++) {
				var child = children[i];
				if (child.className == 'title') {
					title = child.title;
					break;
				}
			}
			var videoId = element.href.replace(/^[^v]+v.(.{11}).*/,"$1");
			ids.push([title, videoId]);
		});

		return ids;
	};

	var displayModalWindow = function() {
		var ytIds = grabYouTubeIds();
		var dispStr = 'Found IDs:\n';
		$.each(ytIds, function(index, element) {
			dispStr += element[0] + ': ' + element[1] + '\n';
		});
		alert(dispStr);
	};

	if (!($ = window.jQuery)) { /* typeof jQuery=='undefined' works too */
		script = document.createElement('script');
		script.src = 'http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js';
		script.onload=displayModalWindow;
		document.body.appendChild(script);
	} else {
		displayModalWindow();
	}
})());