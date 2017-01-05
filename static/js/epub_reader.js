
var reader = null;

function EpubReader(epubUrl) {
    Reader.call(this, "iframe", "#ebookHolder");
    this.epub = ePub(epubUrl);
    this.epub.renderTo("ebookHolder");;
}

EpubReader.prototype = Object.create(Reader.prototype);
EpubReader.prototype.constructor = EpubReader;

EpubReader.prototype.prevPage = function () {
    this.epub.prevPage();
};

EpubReader.prototype.nextPage = function () {
    this.epub.nextPage();
};

function readEpub(epubUrl) {
    reader = new EpubReader(epubUrl);
    reader.setup();
    reader.fitVertical();
}