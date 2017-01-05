

var reader = null;
var scale = 0.8;

function PdfReader(pdfFileId) {
    Reader.call(this, "#pdf-canvas", "#pdf-holder");
    this.context = this.container[0].getContext('2d');
    this.pageNum = 1;
    this.pageNumPending = null;
    this.pageRendering = false;
    var self = this;
    PDFJS.getDocument('/file/' + pdfFileId).then(function (pdfDoc_) {
        self.pdfDoc = pdfDoc_;
        $('#page_count').text(pdfDoc_.numPages);

        // Initial/first page rendering
        self.renderPage(self.pageNum);
    });
}

PdfReader.prototype = Object.create(Reader.prototype);
PdfReader.prototype.constructor = PdfReader;

PdfReader.prototype.renderPage = function(num) {
    this.pageRendering = true;
    // Using promise to fetch the page
    var self = this;
    this.pdfDoc.getPage(num).then(function (page) {
        var viewport = page.getViewport(scale);
        self.container.height = viewport.height;
        self.container.width = viewport.width;

        // Render PDF page into canvas context
        var renderContext = {
            canvasContext: self.context,
            viewport: viewport
        };
        var renderTask = page.render(renderContext);

        // Wait for rendering to finish
        renderTask.promise.then(function () {
            self.pageRendering = false;
            if (self.pageNumPending !== null) {
                // New page rendering is pending
                self.renderPage(self.pageNumPending);
                self.pageNumPending = null;
            }
        });
    });

    // Update page counters
    $('#page_num').text(this.pageNum);
};

PdfReader.prototype.queueRenderPage = function(num) {
    if (this.pageRendering) {
        this.pageNumPending = num;
    } else {
        this.renderPage(num);
    }
};

PdfReader.prototype.prevPage = function() {
    if (this.pageNum <= 1) {
        return;
    }
    this.pageNum--;
    this.queueRenderPage(this.pageNum);
};

PdfReader.prototype.nextPage = function() {
    if (this.pageNum >= this.pdfDoc.numPages) {
        return;
    }
    this.pageNum++;
    this.queueRenderPage(this.pageNum);
};

function readPdf(pdfFileId) {
    reader = new PdfReader(pdfFileId);
    reader.setup();
}