var path = require('path');
module.exports = {
    entry: {
        // comic_reader: './js/comic_reader.js',
        // epub_reader: './js/epub_reader.js',
        //pdf_reader: './js/pdf_reader.js'
        app: './js/app.js'
    },
    output: {
        path: path.join(__dirname, "static/js/"),
        filename: '[name]_bundle.js',
    },
    module: {
        loaders: [
            {
                test: /\.js$/,
                include: [
                    path.join(__dirname, "js/"),
                ],
                loader: 'babel-loader'
            }
        ]
    }
};