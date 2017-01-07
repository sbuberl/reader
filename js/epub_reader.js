
import { Reader } from "./reader";

export class EpubReader extends Reader {
    constructor(epubUrl) {
        super("iframe", "#ebookHolder");
        this.epub = ePub(epubUrl);
        this.epub.renderTo("ebookHolder");;
    }

    prevPage() {
        this.epub.prevPage();
    }

    nextPage() {
        this.epub.nextPage();
    }
}

let reader = null;
export function readEpub(epubUrl) {
    reader = new EpubReader(epubUrl);
    reader.setup();
    reader.fitVertical();
}