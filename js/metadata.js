import React from 'react';
import Store from './store';

export default class MetadataForm extends React.Component {
    constructor (props) {
        super(props);

        this.docStore = new Store("documents");
    }

    render () {
        const document = this.docStore.items.find(doc => doc.id == this.props.params.doc);
        const isComic = document.type == 'comic';
        return (
            <div>
                <h1>Edit Metadata</h1>

                <form action="" method='post' encType='multipart/form-data'>

                    {!isComic ? (
                         <div>
                            <label htmlFor="name">Name</label>
                            <input className="form-control" id="name" name="name" type="text" value={document.name || ''} />>
                        </div>
                    ) : (
                        <div>
                            <label htmlFor="series">Series</label>
                            <input className="form-control" id="series" name="series" type="text" value={document.series || ''} />

                            <label htmlFor="issue">Issue</label>
                            <input className="form-control" id="issue" name="issue" type="text" value={document.issue || ''} />
                        </div>
                    )}

                    <label htmlFor="author">Author</label>
                    <input className="form-control" id="author" name="author" type="text" value={document.author || ''} />

                    <label htmlFor="publisher">Publisher</label>
                    <input className="form-control" id="publisher" name="publisher" type="text" value={document.publisher || ''} />

                    <label htmlFor="release_date">Release Date</label>
                    <input className="form-control" id="release_date" name="release_date" type="date" value="" />

                    <button type="submit" className="btn btn-primary">Save</button>
                    <button href="/" className="btn btn-danger">Cancel</button>

                </form>
            </div>
        )
    }
}
