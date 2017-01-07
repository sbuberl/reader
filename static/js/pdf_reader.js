var GlobalAccess = GlobalAccess || {}; GlobalAccess["pdf_reader"] =
/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};

/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {

/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId])
/******/ 			return installedModules[moduleId].exports;

/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			exports: {},
/******/ 			id: moduleId,
/******/ 			loaded: false
/******/ 		};

/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);

/******/ 		// Flag the module as loaded
/******/ 		module.loaded = true;

/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}


/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;

/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;

/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";

/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(0);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ function(module, exports, __webpack_require__) {

	var __WEBPACK_AMD_DEFINE_ARRAY__, __WEBPACK_AMD_DEFINE_RESULT__;!(__WEBPACK_AMD_DEFINE_ARRAY__ = [exports, __webpack_require__(1)], __WEBPACK_AMD_DEFINE_RESULT__ = function (exports, _reader) {
	    "use strict";

	    Object.defineProperty(exports, "__esModule", {
	        value: true
	    });
	    exports.PdfReader = undefined;
	    exports.readPdf = readPdf;

	    function _classCallCheck(instance, Constructor) {
	        if (!(instance instanceof Constructor)) {
	            throw new TypeError("Cannot call a class as a function");
	        }
	    }

	    var _createClass = function () {
	        function defineProperties(target, props) {
	            for (var i = 0; i < props.length; i++) {
	                var descriptor = props[i];
	                descriptor.enumerable = descriptor.enumerable || false;
	                descriptor.configurable = true;
	                if ("value" in descriptor) descriptor.writable = true;
	                Object.defineProperty(target, descriptor.key, descriptor);
	            }
	        }

	        return function (Constructor, protoProps, staticProps) {
	            if (protoProps) defineProperties(Constructor.prototype, protoProps);
	            if (staticProps) defineProperties(Constructor, staticProps);
	            return Constructor;
	        };
	    }();

	    function _possibleConstructorReturn(self, call) {
	        if (!self) {
	            throw new ReferenceError("this hasn't been initialised - super() hasn't been called");
	        }

	        return call && (typeof call === "object" || typeof call === "function") ? call : self;
	    }

	    function _inherits(subClass, superClass) {
	        if (typeof superClass !== "function" && superClass !== null) {
	            throw new TypeError("Super expression must either be null or a function, not " + typeof superClass);
	        }

	        subClass.prototype = Object.create(superClass && superClass.prototype, {
	            constructor: {
	                value: subClass,
	                enumerable: false,
	                writable: true,
	                configurable: true
	            }
	        });
	        if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass;
	    }

	    var reader = null;
	    var scale = 0.8;

	    var PdfReader = exports.PdfReader = function (_Reader) {
	        _inherits(PdfReader, _Reader);

	        function PdfReader(pdfFileId) {
	            _classCallCheck(this, PdfReader);

	            var _this = _possibleConstructorReturn(this, (PdfReader.__proto__ || Object.getPrototypeOf(PdfReader)).call(this, "#pdf-canvas", "#pdf-holder"));

	            var canvas = _this.container[0];
	            _this.context = canvas.getContext('2d');
	            _this.pageNum = 1;
	            _this.pageNumPending = null;
	            _this.pageRendering = false;
	            var self = _this;
	            PDFJS.getDocument('/file/' + pdfFileId).then(function (pdfDoc_) {
	                self.pdfDoc = pdfDoc_;
	                $('#page_count').text(pdfDoc_.numPages);

	                // Initial/first page rendering
	                self.renderPage(self.pageNum);
	            });
	            return _this;
	        }

	        _createClass(PdfReader, [{
	            key: "renderPage",
	            value: function renderPage(num) {
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
	            }
	        }, {
	            key: "queueRenderPage",
	            value: function queueRenderPage(num) {
	                if (this.pageRendering) {
	                    this.pageNumPending = num;
	                } else {
	                    this.renderPage(num);
	                }
	            }
	        }, {
	            key: "prevPage",
	            value: function prevPage() {
	                if (this.pageNum <= 1) {
	                    return;
	                }
	                this.pageNum;
	                this.queueRenderPage(this.pageNum);
	            }
	        }, {
	            key: "nextPage",
	            value: function nextPage() {
	                if (this.pageNum >= this.pdfDoc.numPages) {
	                    return;
	                }
	                this.pageNum++;
	                this.queueRenderPage(this.pageNum);
	            }
	        }]);

	        return PdfReader;
	    }(_reader.Reader);

	    function readPdf(pdfFileId) {
	        reader = new PdfReader(pdfFileId);
	        reader.setup();
	    }
	}.apply(exports, __WEBPACK_AMD_DEFINE_ARRAY__), __WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));

/***/ },
/* 1 */
/***/ function(module, exports, __webpack_require__) {

	var __WEBPACK_AMD_DEFINE_ARRAY__, __WEBPACK_AMD_DEFINE_RESULT__;!(__WEBPACK_AMD_DEFINE_ARRAY__ = [exports], __WEBPACK_AMD_DEFINE_RESULT__ = function (exports) {
	    "use strict";

	    Object.defineProperty(exports, "__esModule", {
	        value: true
	    });

	    function _classCallCheck(instance, Constructor) {
	        if (!(instance instanceof Constructor)) {
	            throw new TypeError("Cannot call a class as a function");
	        }
	    }

	    var _createClass = function () {
	        function defineProperties(target, props) {
	            for (var i = 0; i < props.length; i++) {
	                var descriptor = props[i];
	                descriptor.enumerable = descriptor.enumerable || false;
	                descriptor.configurable = true;
	                if ("value" in descriptor) descriptor.writable = true;
	                Object.defineProperty(target, descriptor.key, descriptor);
	            }
	        }

	        return function (Constructor, protoProps, staticProps) {
	            if (protoProps) defineProperties(Constructor.prototype, protoProps);
	            if (staticProps) defineProperties(Constructor, staticProps);
	            return Constructor;
	        };
	    }();

	    var Reader = exports.Reader = function () {
	        function Reader(container, parent) {
	            _classCallCheck(this, Reader);

	            this.container = $(container);
	            this.parent = $(parent);
	        }

	        _createClass(Reader, [{
	            key: "setup",
	            value: function setup() {
	                var self = this;
	                $("#prevPanel").on("click", self.prevPage.bind(self));
	                $("#nextPanel").on("click", self.nextPage.bind(self));
	                $("#fitVertical").on("click", self.fitVertical.bind(self));
	                $("#fitHorizontal").on("click", self.fitHorizontal.bind(self));
	                $("#fitBoth").on("click", self.fitBoth.bind(self));
	                this.fitHorizontal();

	                if ('ontouchstart' in window // works on most browsers
	                || navigator.maxTouchPoints) {
	                    container.swipeEvents().bind("swipeLeft", self.prevPage.bind(self)).bind("swipeRight", self.nextPage.bind(self));
	                }
	            }
	        }, {
	            key: "prevPage",
	            value: function prevPage() {
	                throw new TypeError("prevPage not implemented");
	            }
	        }, {
	            key: "nextPage",
	            value: function nextPage() {
	                throw new TypeError("nextPage not implemented");
	            }
	        }, {
	            key: "fitHorizontal",
	            value: function fitHorizontal() {
	                this.parent.removeClass();
	                this.container.removeClass();
	                this.container.addClass('fitHorizontal');
	            }
	        }, {
	            key: "fitVertical",
	            value: function fitVertical() {
	                this.container.removeClass();
	                this.container.addClass('fitVertical');
	                this.parent.addClass('fit');
	            }
	        }, {
	            key: "fitBoth",
	            value: function fitBoth() {
	                this.container.removeClass();
	                this.container.addClass('fitBoth');
	                this.parent.addClass('fit');
	            }
	        }]);

	        return Reader;
	    }();
	}.apply(exports, __WEBPACK_AMD_DEFINE_ARRAY__), __WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));

/***/ }
/******/ ]);