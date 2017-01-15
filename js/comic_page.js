import React from 'react';

export default class ComicPage extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <img id="reader-content" ref="reader-content" src={"/comic/" + this.props.comic + "/page/" + this.props.page} className={this.props.readerClass} />
        )
    }
}
