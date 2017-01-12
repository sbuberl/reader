import React from 'react';
import ComicPage from './comic_page';
import ReaderNavbar from './reader_navbar';

export default class ComicReader extends React.Component {
    constructor(props) {
        super(props);

        this.state = {
            pageNumber: 1,
            wrapperClass: "fit",
            readerClass: "fitVertical"
        };

        this.previousPage = this.previousPage.bind(this);
        this.nextPage = this.nextPage.bind(this);
        this.onFitChange = this.onFitChange.bind(this);
    }

    previousPage() {
        if(this.state.pageNumber > 1) {
            this.setState({pageNumber: this.state.pageNumber - 1});
        }
    }

    nextPage() {
        if(this.state.pageNumber < this.props.pageCount) {
            this.setState({pageNumber: this.state.pageNumber + 1});
        }
    }

    onFitChange(reader, wrapper) {
        this.setState({readerClass: reader, wrapperClass: wrapper});
    }

    render() {
        return (
            <div id="reader">
                <ReaderNavbar onPrevious={this.previousPage} onNext={this.nextPage} onFitChange={this.onFitChange} />
                <div id="reader-wrapper" className={this.state.wrapperClass} >
                    <ComicPage comic={this.props.comic} page={this.state.pageNumber} readerClass={this.state.readerClass} />
                </div>
            </div>
        )
    }
}
