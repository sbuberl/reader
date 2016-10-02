var pdfDoc = null,
    pageNum = 1,
    pageRendering = false,
    pageNumPending = null,
    scale = 0.8,
    canvas = null,
    ctx = null;

/**
* Get page info from document, resize canvas accordingly, and render page.
* @param num Page number.
*/
function renderPage(num) {
    pageRendering = true;
    // Using promise to fetch the page
    pdfDoc.getPage(num).then(function(page) {
        var viewport = page.getViewport(scale);
        canvas.height = viewport.height;
        canvas.width = viewport.width;

        // Render PDF page into canvas context
        var renderContext = {
            canvasContext: ctx,
            viewport: viewport
        };
        var renderTask = page.render(renderContext);

        // Wait for rendering to finish
        renderTask.promise.then(function () {
            pageRendering = false;
            if (pageNumPending !== null) {
                // New page rendering is pending
                renderPage(pageNumPending);
                pageNumPending = null;
            }
        });
    });

    // Update page counters
    $('#page_num').text(pageNum);
}

/**
* If another page rendering in progress, waits until the rendering is
* finised. Otherwise, executes rendering immediately.
*/
function queueRenderPage(num) {
    if (pageRendering) {
        pageNumPending = num;
    } else {
        renderPage(num);
    }
}

/**
* Displays previous page.
*/
function onPrevPage() {
    if (pageNum <= 1) {
        return;
    }
    pageNum--;
    queueRenderPage(pageNum);
}

/**
* Displays next page.
*/
function onNextPage() {
    if (pageNum >= pdfDoc.numPages) {
        return;
    }
    pageNum++;
    queueRenderPage(pageNum);
}

function fitHorizontal() {
  $("#pdf-holder").removeClass();
  $("#pdf-canvas").removeClass();
  $("#pdf-canvas").addClass('fitHorizontal');
}

function fitVertical() {
  $("#pdf-canvas").removeClass();
  $("#pdf-canvas").addClass('fitVertical');
  $("#pdf-holder").addClass('fit');

}
function fitBoth() {
  $("#pdf-canvas").removeClass();
  $("#pdf-canvas").addClass('fitBoth');
  $("#pdf-holder").addClass('fit');
}
function readPdf(pdfFileId) {
    canvas = document.getElementById('pdf-canvas');
    ctx = canvas.getContext('2d');

    $('#prev').on('click', onPrevPage);
    $('#next').on('click', onNextPage);

     if(isTouchDevice()) {
        $('#page')
          .swipeEvents()
          .bind("swipeLeft",  prevPage)
          .bind("swipeRight", nextPage);
    }

    $("#fitVertical").on("click",fitVertical);
    $("#fitHorizontal").on("click",fitHorizontal);
    $("#fitBoth").on("click",fitBoth);

    PDFJS.getDocument('/file/' + pdfFileId).then(function (pdfDoc_) {
        pdfDoc = pdfDoc_;
        $('#page_count').text(pdfDoc.numPages);

        // Initial/first page rendering
        renderPage(pageNum);
    });
}