import { Reader } from "./reader";

let reader = null;
const scale = 0.8;

export class PdfReader extends Reader {
    constructor(pdfFileId) {
        super("#pdf-canvas", "#pdf-holder");
        let canvas = this.container[0];
        this.context = canvas.getContext('2d');
        this.pageNum = 1;
        this.pageNumPending = null;
        this.pageRendering = false;
        let self = this;
        PDFJS.getDocument('/file/' + pdfFileId).then(function (pdfDoc_) {
            self.pdfDoc = pdfDoc_;
            $('#page_count').text(pdfDoc_.numPages);

            // Initial/first page rendering
            self.renderPage(self.pageNum);
        });
    }

    renderPage(num) {
        this.pageRendering = true;
        // Using promise to fetch the page
        let self = this;
        this.pdfDoc.getPage(num).then(function (page) {
            let viewport = page.getViewport(scale);
            self.container.height = viewport.height;
            self.container.width = viewport.width;

            // Render PDF page into canvas context
            let renderContext = {
                canvasContext: self.context,
                viewport: viewport
            };
            let renderTask = page.render(renderContext);

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
    }

    queueRenderPage(num) {
        if (this.pageRendering) {
            this.pageNumPending = num;
        } else {
            this.renderPage(num);
        }
    }

    prevPage() {
        if (this.pageNum <= 1) {
            return;
        }
        this.pageNum;
        this.queueRenderPage(this.pageNum);
    }

    nextPage() {
        if (this.pageNum >= this.pdfDoc.numPages) {
            return;
        }
        this.pageNum++;
        this.queueRenderPage(this.pageNum);
    }
}

export function readPdf(pdfFileId) {
    reader = new PdfReader(pdfFileId);
    reader.setup();
}
