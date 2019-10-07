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
            prodImages: {},
            selectedDev: [],
            selectedProd: []
        }
        this.getReposData()
    }

    getReposData() {
        axios.get('http://localhost:8080/api/images/dev').then(res => {
            const images = res.data
            this.setState({
                devImages: images
            })
        })
        axios.get('http://localhost:8080/api/images/prod').then(res => {
            const images = res.data
            this.setState({
                prodImages: images
            })
        })
    }

    handleChangeMultiple(event) {
        const { options } = event.target;
        const value = [];
        for (let i = 0, l = options.length; i < l; i += 1) {
            if (options[i].selected) {
                value.push(options[i].value);
            }
        }
        return value
    }

    moveImage(image) {
        const { selectedDev, selectedProd } = this.state
        let selected = selectedDev
        let url = 'prod'
        if (selectedProd.length > 0) {
            selected = selectedProd
            url = 'dev'
        }
        if (selected.length === 0) alert('Choose image(s)');
        axios.post('http://localhost:8080/api/move/to_' + url, {
            images: selected
        }).then(res => {
            this.getReposData()
        })
    }

    removeImage() {
        const { selectedDev, selectedProd } = this.state
        let selected = selectedDev
        let url = 'dev'
        if (selectedProd.length > 0) {
            selected = selectedProd
            url = 'prod'
        }
        if (selected.length === 0) alert('Choose image(s)');
        axios.post('http://localhost:8080/api/remove/' + url, {
            images: selected
        }).then(res => {
            this.getReposData()
        })
    }

    changeTag(image, newTag) {

    }

    render() {
        const {devImages, prodImages, selectedDev, selectedProd} = this.state
        return (
            <div className='App'>
                <div className='images-list'>
                    <ImagesList
                        images={devImages}
                        title="dev"
                        selected={selectedDev}
                        handleChange={(event) => {
                            this.setState({
                                selectedProd: [],
                                selectedDev: this.handleChangeMultiple(event)
                            })
                        }}
                    />
                </div>
                <div className='actions-list'>
                    <div className='button-wrapper'>
                        <Button
                            variant="contained"
                            color="primary"
                            onClick={()=>{this.moveImage()}}
                            endIcon={<ArrowForward />}
                        >
                            Move to prod
                        </Button>
                    </div>
                    <div className='button-wrapper'>
                        <Button
                            variant="contained"
                            color="primary"
                            onClick={()=>{this.moveImage()}}
                            startIcon={<ArrowBack />}
                        >
                            Move to dev
                        </Button>
                    </div>
                    <div className='button-wrapper'>
                        <Button
                            variant="contained"
                            color="secondary"
                            onClick={()=>{this.removeImage()}}
                            endIcon={<Delete />}
                        >
                            remove
                        </Button>
                    </div>
                </div>
                <div className='images-list'>
                    <ImagesList
                        images={prodImages}
                        title="prod"
                        selected={selectedProd}
                        handleChange={(event) => {
                            this.setState({
                                selectedDev: [],
                                selectedProd: this.handleChangeMultiple(event)
                            })
                        }}
                    />
                </div>
            </div>
        );
    }
}

export default App;
