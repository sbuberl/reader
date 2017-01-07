var GlobalAccess = GlobalAccess || {}; GlobalAccess["comic_reader"] =
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
	    exports.ComicReader = undefined;
	    exports.readComic = readComic;

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

	    var ComicReader = exports.ComicReader = function (_Reader) {
	        _inherits(ComicReader, _Reader);

	        function ComicReader(comicId, pageCount) {
	            _classCallCheck(this, ComicReader);

	            var _this = _possibleConstructorReturn(this, (ComicReader.__proto__ || Object.getPrototypeOf(ComicReader)).call(this, "#page", "#pageHolder"));

	            _this.comicId = comicId;
	            _this.pageCount = pageCount;
	            _this.page = 1;
	            return _this;
	        }

	        _createClass(ComicReader, [{
	            key: "displayPage",
	            value: function displayPage() {
	                this.container.attr("src", "/comic/" + this.comicId + "/page/" + this.page);
	            }
	        }, {
	            key: "prevPage",
	            value: function prevPage() {
	                if (this.page > 1) {
	                    this.page -= 1;
	                    this.displayPage();
	                }
	            }
	        }, {
	            key: "nextPage",
	            value: function nextPage() {
	                if (this.page < this.pageCount) {
	                    this.page += 1;
	                    this.displayPage();
	                }
	            }
	        }]);

	        return ComicReader;
	    }(_reader.Reader);

	    var reader = null;
	    function readComic(comicId, pageCount) {
	        reader = new ComicReader(comicId, pageCount);
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