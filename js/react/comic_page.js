import React from 'react';

export default class ComicPage extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        rreturn (
            <img id="reader-content" src={"http://localhost:5000/comic/" + this.props.comic + "/page/" + this.props.page} className={this.props.readerClass} />
        )
    }
}
