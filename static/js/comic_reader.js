
var reader;

function ComicReader(comicId, pageCount) {
    Reader.call(this, "#page", "#pageHolder");
    this.comicId = comicId;
    this.pageCount = pageCount;
    this.page = 1;
}

ComicReader.prototype = Object.create(Reader.prototype);
ComicReader.prototype.constructor = ComicReader;

ComicReader.prototype.displayPage = function() {
    $("#page").attr("src", "/comic/" + this.comicId + "/page/" + this.page);
};

ComicReader.prototype.prevPage = function() {
    if(this.page > 1) {
        this.page -= 1;
        this.displayPage();
    }
};

ComicReader.prototype.nextPage = function() {
    if(this.page < this.pageCount) {
        this.page += 1;
        this.displayPage();
    }
};

function readComic(comicId, pageCount) {
    reader = new ComicReader(comicId, pageCount);
    reader.setup();
}
