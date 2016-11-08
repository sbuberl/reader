
var epub = null;

function prevPage()
{
    epub.prevPage();
}

function nextPage()
{
    epub.nextPage();
}

function fitHorizontal() {
  $("#ebookHolder").removeClass();
  $("iframe").removeClass();
  $("iframe").addClass('fitHorizontal');
}

function fitVertical() {
  $("iframe").removeClass();
  $("iframe").addClass('fitVertical');
  $("#ebookHolder").addClass('fit');

}

function fitBoth() {
    $("iframe").removeClass();
    $("iframe").addClass('fitBoth');
    $("#ebookHolder").addClass('fit');
}

function readEpub(epubUrl) {

    epub = ePub(epubUrl);
    epub.renderTo("ebookHolder");

    $("#prevPanel").on("click", prevPage);
    $("#nextPanel").on("click", nextPage);

    if (isTouchDevice()) {
        $('iframe')
            .swipeEvents()
            .bind("swipeLeft", prevPage)
            .bind("swipeRight", nextPage);
    }

    $("#fitVertical").on("click", fitVertical);
    $("#fitHorizontal").on("click", fitHorizontal);
    $("#fitBoth").on("click", fitBoth);

    fitVertical();




}



