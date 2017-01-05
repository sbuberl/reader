
function Reader(container, parent) {
    this.container = $(container);
    this.parent = $(parent);
}

Reader.prototype.setup = function() {
    var that = this;
    $("#prevPanel").on("click", that.prevPage.bind(that));
    $("#nextPanel").on("click", that.nextPage.bind(that));
    $("#fitVertical").on("click", that.fitVertical.bind(that));
    $("#fitHorizontal").on("click", that.fitHorizontal.bind(that));
    $("#fitBoth").on("click", that.fitBoth.bind(that));
    this.fitHorizontal();

    if('ontouchstart' in window        // works on most browsers
        || navigator.maxTouchPoints) {
        container
            .swipeEvents()
            .bind("swipeLeft",  that.prevPage.bind(that))
            .bind("swipeRight", that.nextPage.bind(that));
    }
};

Reader.prototype.prevPage = function() {
    throw new TypeError("prevPage not implemented");
};

Reader.prototype.nextPage = function() {
    throw new TypeError("nextPage not implemented");
};

Reader.prototype.fitHorizontal = function() {
    this.parent.removeClass();
    this.container.removeClass();
    this.container.addClass('fitHorizontal');
};

Reader.prototype.fitVertical = function() {
    this.container.removeClass();
    this.container.addClass('fitVertical');
    this.parent.addClass('fit');
};

Reader.prototype.fitBoth = function() {
    this.container.removeClass();
    this.container.addClass('fitBoth');
    this.parent.addClass('fit');
};
