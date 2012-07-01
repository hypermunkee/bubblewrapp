                    javascript:void((function() {
                            var grabYouTubeIds = function() {
                                    var ids = new Array();

                                    /* If on a YouTube page, this will grab the primary YouTube ID. */
                                    var url = location.href.replace(/https?:\/\//i, '');
                                    var pattern = /(http:\/\/)?(?:www\.)?youtube.com\/watch\?(?=.*v=[\-\w]+)(?:\S+)?$/;
                                    if (pattern.test(url)) {
                                            var title = $('#eow-title').attr('title');
                                            var videoId = $('input[name="video_id"]').val();
                                            var views = parseInt($(".watch-view-count strong").html().replace(/\D/g,''));
                                            ids.push([title, videoId, views]);
                                    }

                                    /* Grab all related video titles, view counts, and IDs. */
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
                                            for (var i = 0; i < children.length; i++) {
                                                    var child = children[i];
                                                    if (child.className == 'view-count') {
                                                            views = parseInt($(".view-count").html().replace(/\D/g,''));
                                                            break;
                                                    }

                                            }
                                            var views = parseInt($(".view-count").html().replace(/\D/g,''));
                                            var videoId = element.href.replace(/^[^v]+v.(.{11}).*/,"$1");
                                            ids.push([title, videoId, views]);
                                    });

                                    return ids;
                            };

                            var displayModalWindow = function() {
                                    /* Clear the modal window body */
                                    $('.modal-body').empty();
                                    var ytIds = $.unique(grabYouTubeIds());
                                    $.each(ytIds, function(index, element) {
                                            /* Generate a random number between 200 and 400 */
                                            var randomNum = Math.ceil(Math.random()*200)+200;
                                            $(".modal-body").append("<p class='bubblewrapp-image' style='width:"+randomNum+"px;margin:10px;float:left;'>"+
                                            "<img style='float:left;box-shadow: #000 0 2px 10px;' src='http://img.youtube.com/vi/"+element[1]
                                            +"/0.jpg' /><span class='bubblewrapp-image-title' style='float:left;color:#fff;"+
                                            "margin-top:-40px;background-color:rgba(0,0,0,0.7);padding:0 5px;' >"+element[0]+" - "+element[2]+"</span></p>");
                                    });

                                    /* Wait until images are loaded before we apply masonry to them */
                                    var $container = $('.modal-body');
                                    $container.imagesLoaded(function(){
                                      $container.masonry({
                                        itemSelector : '.bubblewrapp-image'
                                      });
                                    }); 

                                    /* Show the modal window */
                                    $('#myModal').modal('show');

                                    /* Highlight the image on click */
                                    $('.bubblewrapp-image').toggle(function(){
                                        $(this).css("border","5px #FAA732 solid");
                                    }, function() {
                                        $(this).css("border","none");
                                    });

                            };



                            if (!($ = window.jQuery)) { /* typeof jQuery=='undefined' works too */
                                    script = document.createElement('script');
                                    script.src = 'http://ajax.googleapis.com/ajax/libs/jquery/1/jquery.min.js';
                                    script.onload=displayModalWindow;
                                    document.body.appendChild(script);
                            } else {
                                    /* Load Twitter bootstrap dependencies & masonry */
                                    $('head').append('<link rel="stylesheet" href="http://www.bubblewrapp.com/static/bootstrap.css" type="text/css" />');
                                    $('head').append('<script type="text/javascript" src="http://www.bubblewrapp.com/static/js/jquery.masonry.min.js" />');
                                    $('head').append('<script type="text/javascript" src="http://www.bubblewrapp.com/static/bootstrap.js" />');

                                    $('body').append('<div style="width:900px !important; margin:-425px 0 0 -450px !important; max-height:1000px !important;" class="modal hide" id="myModal">'+
                                        '<div class="modal-header"><button type="button" class="close" data-dismiss="modal">×</button>'+
                                        '<img src="http://bubblewrapp.herokuapp.com/static/images/logo-small-black.png"'+
                                        ' alt="Bubblewrapp logo" /></div><div class="modal-body"><p>Choose a video to add</p></div>'+
                                        '<div class="modal-footer"><a href="#" class="btn" data-dismiss="modal">Close</a>'+
                                        '<a href="http://bubblewrapp.herokuapp.com/createbundle?params=put+things+here" class="btn btn-primary">Add to bundle</a></div></div>');
                                    displayModalWindow();

                            }
                    })());