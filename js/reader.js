export class Reader {
    constructor(container, parent) {
        this.container = $(container);
        this.parent = $(parent);
    }

    setup() {
        let self = this;
        $("#prevPanel").on("click", self.prevPage.bind(self));
        $("#nextPanel").on("click", self.nextPage.bind(self));
        $("#fitVertical").on("click", self.fitVertical.bind(self));
        $("#fitHorizontal").on("click", self.fitHorizontal.bind(self));
        $("#fitBoth").on("click", self.fitBoth.bind(self));
        this.fitHorizontal();

        if('ontouchstart' in window        // works on most browsers
            || navigator.maxTouchPoints) {
            container
                .swipeEvents()
                .bind("swipeLeft",  self.prevPage.bind(self))
                .bind("swipeRight", self.nextPage.bind(self));
        }
    }

    prevPage() {
        throw new TypeError("prevPage not implemented");
    }

    nextPage() {
        throw new TypeError("nextPage not implemented");
    }

    fitHorizontal() {
      this.parent.removeClass();
      this.container.removeClass();
      this.container.addClass('fitHorizontal');
    }

    fitVertical() {
      this.container.removeClass();
      this.container.addClass('fitVertical');
      this.parent.addClass('fit');
    }

    fitBoth() {
        this.container.removeClass();
        this.container.addClass('fitBoth');
        this.parent.addClass('fit');
    }
}
