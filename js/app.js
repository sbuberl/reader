import React from 'react';
import ReactDOM from 'react-dom';
import { Router, Route, hashHistory } from 'react-router'
//import Router from './router';
import ComicReader from './comic_reader';
import Library from './library';
import UploadForm from './upload';

ReactDOM.render(
    <Router history={hashHistory}>
        <Route path="/" component={Library}/>
        <Route path="/upload" component={UploadForm}/>
        <Route path="/read/comic/:comic" component={ComicReader}/>
    </Router>,
    document.getElementById('example')
);
