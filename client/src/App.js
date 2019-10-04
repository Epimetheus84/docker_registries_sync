import React from 'react'
import axios from 'axios'
import './App.css'
import ImagesList from "./components/ImagesList"
import Button from '@material-ui/core/Button'
import Delete from '@material-ui/icons/Delete'
import ArrowBack from '@material-ui/icons/ArrowBack'
import ArrowForward from '@material-ui/icons/ArrowForward'

class App extends React.Component {

    constructor(props) {
        super(props)
        this.state = {
            devImages: {},
            prodImages: {}
        }
        axios.get('http://localhost:8080/images/dev').then(res => {
            const images = res.data
            this.setState({
                devImages: images
            })
        })
        axios.get('http://localhost:8080/images/prod').then(res => {
            const images = res.data
            this.setState({
                prodImages: images
            })
        })
        this.state = {
            selectedDev: [],
            selectedProd: []
        }
    }

    render() {
        const {devImages, prodImages, selectedDev, selectedProd} = this.state
        return (
            <div className='App'>
                <div className='images-list'>
                    <ImagesList images={devImages} title="dev" />
                </div>
                <div className='actions-list'>
                    <div className='button-wrapper'>
                        <Button
                            variant="contained"
                            color="primary"
                            endIcon={<ArrowForward />}
                        >
                            Move to prod
                        </Button>
                    </div>
                    <div className='button-wrapper'>
                        <Button
                            variant="contained"
                            color="primary"
                            startIcon={<ArrowBack />}
                        >
                            Move to dev
                        </Button>
                    </div>
                    <div className='button-wrapper'>
                        <Button
                            variant="contained"
                            color="secondary"
                            endIcon={<Delete />}
                        >
                            remove
                        </Button>
                    </div>
                </div>
                <div className='images-list'>
                    <ImagesList images={prodImages} title="prod" />
                </div>
            </div>
        );
    }
}

export default App;
