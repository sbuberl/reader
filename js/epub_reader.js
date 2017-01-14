import React from 'react';
import ComicPage from './comic_page';
import {ReactReader} from 'react-reader'

export default class EpubReader extends React.Component {
   constructor (props) {
    super(props)
    this.state = {
      fullscreen: false
    }
  }

  toggleFullscreen = () => {
    this.setState({
      fullscreen: !this.state.fullscreen
    }, () => {
      setTimeout(() => {
        const evt = document.createEvent('UIEvents')
        evt.initUIEvent('resize', true, false, global, 0)
        global.dispatchEvent(evt)
      }, 1000)
    })
  }

  render () {
    const {fullscreen} = this.state
    return (
        <div style={{position: 'relative', height: '100vh'}}>
            <ReactReader
                url={'http://localhost:5000/epub/1/'}
                title={'Dracula'}
            />
        </div>
    )
  }
}
