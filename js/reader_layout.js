import React from 'react';
import ComicReader from './comic_reader';

module.exports = class ReaderLayout extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        return (
            <ComicReader comic={2} pageCount={37} />
        )
    }
}
