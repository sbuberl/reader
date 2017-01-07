
import { Reader } from "./reader";

export class ComicReader extends Reader {
    constructor(comicId, pageCount) {
        super("#page", "#pageHolder");
        this.comicId = comicId;
        this.pageCount = pageCount;
        this.page = 1;
    }

    displayPage() {
        this.container.attr("src", "/comic/" + this.comicId + "/page/" + this.page);
    }

    prevPage() {
        if(this.page > 1) {
            this.page -= 1;
            this.displayPage();
        }
    }

    nextPage() {
        if(this.page < this.pageCount) {
            this.page += 1;
            this.displayPage();
        }
    }
}

let reader = null;
export function readComic(comicId, pageCount) {
    reader = new ComicReader(comicId, pageCount);
    reader.setup();
}


