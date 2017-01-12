import React from 'react';

export default class ReaderNavbar extends React.Component {
    constructor(props) {
        super(props);
        this.container = $("#reader-content");
        this.parent = $("#reader-wrapper");

        this.fitHorizontal = this.fitHorizontal.bind(this);
        this.fitBoth = this.fitBoth.bind(this);
        this.fitVertical = this.fitVertical.bind(this);
    }

    fitHorizontal() {
        this.props.onFitChange('fitHorizontal', 'none');
    }

    fitVertical() {
        this.props.onFitChange('fitVertical', 'fit');
    }

    fitBoth() {
        this.props.onFitChange('fitBoth', 'fit');
    }

    render() {
        return (
            <nav className="navbar navbar-default navbar-fixed-top">
                <div className="container">
                    <div className="navbar-header">
                        <button type="button" className="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
                        <span className="sr-only">Toggle navigation</span>
                        <span className="icon-bar"></span>
                        <span className="icon-bar"></span>
                        <span className="icon-bar"></span>
                        </button>
                        <a className="navbar-brand" href="#">Reader</a>
                    </div>
                    <div id="navbar" className="navbar-collapse collapse">
                        <ul className="nav navbar-nav">
                        <li><a href="#" id="prevPanel" onClick={this.props.onPrevious}><span className="glyphicon glyphicon-chevron-left"></span> Previous</a></li>
                        <li><a href="#" id="nextPanel" onClick={this.props.onNext}><span className="glyphicon glyphicon-chevron-right icon-white"></span> Next</a></li>
                        <li><a href="#" id="fitVertical" onClick={this.fitVertical}><span className="glyphicon glyphicon-resize-vertical"></span> Fit Vertical</a></li>
                        <li><a href="#" id="fitHorizontal" onClick={this.fitHorizontal}><span className="glyphicon glyphicon-resize-horizontal"></span> Fit Horizontal</a></li>
                        <li><a href="#" id="fitBoth" onClick={this.fitBoth}><span className="glyphicon glyphicon-move"></span> Fit Both</a></li>
                        </ul>
                    </div>
                </div>
            </nav>
        )
    }
}
