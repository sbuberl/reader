import React from 'react';
import 'whatwg-fetch';

export default class Library extends React.Component {
    constructor (props) {
        super(props)

        this.state = {
          documents: []
        };
    }

    componentDidMount() {
        let self = this;
        fetch('/api/documents')
            .then(function(response) {
                return response.json()
            }).then(function(json) {
                self.setState({ documents: json.documents });
            }).catch(function(ex) {
                console.log('parsing failed', ex)
            });
    }

  render () {
    return (
        <div className="container">
            <div className="row">
                <div className="col-lg-12">
                    <h1 className="page-header">Library</h1>
                </div>
            </div>
            <div className="row">
                {this.state.documents.map(document =>
                    <div key={document.id} className="col-lg-3 col-md-3 col-xs-3">
                        <a className="thumbnail" href={"/read/" + document.type + "/" + document.id }>
                            <img className="img-responsive" src={"/file/" + document.cover_id} alt="" />
                            <p>{ document.name }</p>
                        </a>
                        <p>
                            <a href={"/metadata/" + document.type + "/" + document.id}><span className="glyphicon glyphicon-edit"></span> Information</a>
                            <a href={"/download/" + document.type + "/" + document.id}><span className="glyphicon glyphicon-download-alt"></span> Download</a>
                        </p>
                    </div>
                )}
            </div>
        </div>
    )
  }
}