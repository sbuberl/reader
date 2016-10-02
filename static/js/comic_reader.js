
var page = 1;
var pageCount;
var comicId;

function displayPage() {
    $("#page").attr("src", "/comic/" + comicId + "/page/" + page);
}

function prevPage() {
    if (page > 1) {
        page -= 1;
        displayPage(comicId);
    }
}

function nextPage() {
    if (page < pageCount) {
        page += 1;
        displayPage(comicId);
    }
}

function fitHorizontal() {
  $("#pageHolder").removeClass();
  $("#page").removeClass();
  $("#page").addClass('fitHorizontal');
}

function fitVertical() {
  $("#page").removeClass();
  $("#page").addClass('fitVertical');
  $("#pageHolder").addClass('fit');

}
function fitBoth() {
  $("#page").removeClass();
  $("#page").addClass('fitBoth');
  $("#pageHolder").addClass('fit');
}

function readComic(comic, pages) {
    comicId = comic;
    pageCount = pages;
    $("#prevPanel").on("click", prevPage);
    $("#nextPanel").on("click", nextPage);

    if(isTouchDevice()) {
        $('#page')
          .swipeEvents()
          .bind("swipeLeft",  prevPage)
          .bind("swipeRight", nextPage);
    }

    $("#fitVertical").on("click",fitVertical);
    $("#fitHorizontal").on("click",fitHorizontal);
    $("#fitBoth").on("click",fitBoth);

    fitHorizontal();

}
