import React from 'react';

export default class UploadForm extends React.Component {
    constructor (props) {
        super(props);
    }

    render () {
        return (
            <div>
                <h1>Upload new File</h1>
                <form action="/api/documents" method='post' encType='multipart/form-data'>
                    <label htmlFor="uploaded_file">Your document</label>
                    <input className="form-control" id="uploaded_file" name="uploaded_file" type="file" />
                    <button type="submit" className="btn btn-primary">Upload</button>
                </form>
            </div>
        )
    }
}
