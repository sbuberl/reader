
function displayPage(comic_id, page) {
    $("#pageImage img").attr("src", "/comic/" + comic_id + "/page/" + page);
}

function prevPage(page) {
  $("#pageImage").removeClass();
  $("#pageImage img").removeClass();
  $("#pageImage img").addClass('fitHorizontal');
}

function nextPage(page) {
  $("#pageImage").removeClass();
  $("#pageImage img").removeClass();
  $("#pageImage img").addClass('fitHorizontal');
}

function fitHorizontal() {
  $("#pageImage").removeClass();
  $("#pageImage img").removeClass();
  $("#pageImage img").addClass('fitHorizontal');
}

function fitVertical() {
  $("#pageImage img").removeClass();
  $("#pageImage img").addClass('fitVertical');
  $("#pageImage").addClass('fit');

}
function fitBoth() {
  $("#pageImage img").removeClass();
  $("#pageImage img").addClass('fitBoth');
  $("#pageImage").addClass('fit');
}

function readComic(comic_id, pageCount) {
    var page = 1;

    $("#prevPanel").on("click", function() {
        if (page > 1) {
            page -= 1;
            displayPage(comic_id, page);
        }
    });

    $("#nextPanel").on("click", function() {
        if (page < pageCount) {
            page += 1;
            displayPage(comic_id, page);
        }
    });

    $("#fitVertical").on("click",fitVertical);
    $("#fitHorizontal").on("click",fitHorizontal);
    $("#fitBoth").on("click",fitBoth);

    fitHorizontal();

}
