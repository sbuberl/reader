import React from 'react';
import ReactDOM from 'react-dom';
import { Router, Route, hashHistory } from 'react-router'
//import Router from './router';
import ComicReader from './comic_reader';
import Library from './library';
import MetadataForm from './metadata';
import UploadForm from './upload';

ReactDOM.render(
    <Router history={hashHistory}>
        <Route path="/" component={Library}/>
        <Route path="/upload" component={UploadForm}/>
        <Route path="/read/comic/:comic" component={ComicReader}/>
        <Route path="/metadata/:doc" component={MetadataForm}/>
    </Router>,
    document.getElementById('example')
);
