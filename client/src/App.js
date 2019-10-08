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
            srcImages: {},
            dstImages: {},
            selectedDev: [],
            selectedProd: [],
            semWaiting: 2
        }
        this.getReposData()
    }

    getReposData() {
        axios.get('http://localhost:8080/api/images/src').then(res => {
            const images = res.data
            this.setState({
                srcImages: images,
                semWaiting: this.state.semWaiting - 1
            })
        }).catch(err => {
            console.log(err)
            this.setState({
                semWaiting: this.state.semWaiting - 1
            })
        })

        axios.get('http://localhost:8080/api/images/dst').then(res => {
            const images = res.data
            this.setState({
                dstImages: images,
                semWaiting: this.state.semWaiting - 1
            })
        }).catch(err => {
            console.log(err)
            this.setState({
                semWaiting: this.state.semWaiting - 1
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
        let url = 'dst'
        if (selectedProd.length > 0) {
            selected = selectedProd
            url = 'src'
        }
        if (selected.length === 0) alert('Choose image(s)');
        this.setState({
            semWaiting: 2
        })
        axios.post('http://localhost:8080/api/move/to_' + url, {
            images: selected
        }).then(res => {
            this.getReposData()
        })
    }

    removeImage() {
        const { selectedDev, selectedProd } = this.state
        let selected = selectedDev
        let url = 'src'
        if (selectedProd.length > 0) {
            selected = selectedProd
            url = 'dst'
        }
        if (selected.length === 0) alert('Choose image(s)');
        this.setState({
            semWaiting: 2
        })

        let proceed = 0
        for (const image of selected) {
            axios.post('http://localhost:8080/api/remove/' + url, {
                image: image
            }).then(res => {
                const data = res.data
                if (data.status === 'warning') {
                    console.log(data)
                    const duplicates = data.duplicates.join('\n')
                    const force = window.confirm(
                        'Внимание! \n' +
                        'Удалив этот тег, вы также удалите его дупликаты:\n' +
                        duplicates +
                        '\n' +
                        'Продолжить?'
                    )
                    if (force === true) {
                        axios.post('http://localhost:8080/api/remove/' + url, {
                            image: image,
                            force: 1
                        }).then(res => {
                            if (++proceed === selected.length) this.getReposData()
                        }).catch(err => {
                            console.log(err)
                            if (++proceed === selected.length) this.getReposData()
                        })
                    } else {
                        if (++proceed === selected.length) this.getReposData()
                    }
                    return
                }
                if (++proceed === selected.length) this.getReposData()
            }).catch(err => {
                console.log(err)
                if (++proceed === selected.length) this.getReposData()
            })
        }
    }

    render() {
        const {srcImages, dstImages, selectedDev, selectedProd, semWaiting} = this.state
        console.log(semWaiting)
        return (
            <div className='App'>
                { semWaiting > 0 && <div className='preloader'>
                    <div className="lds-ring"><div></div><div></div><div></div><div></div></div>
                </div> }
                <div className='images-list'>
                    <ImagesList
                        images={srcImages}
                        title="src"
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
                    { selectedDev.length > 0 && <div className='button-wrapper'>
                        <Button
                            variant="contained"
                            color="primary"
                            onClick={()=>{this.moveImage()}}
                            endIcon={<ArrowForward />}
                        >
                            Копировать на dev
                        </Button>
                    </div>}
                    { selectedProd.length > 0 && <div className='button-wrapper'>
                        <Button
                            variant="contained"
                            color="primary"
                            onClick={()=>{this.moveImage()}}
                            startIcon={<ArrowBack />}
                        >
                            Копировать на prod
                        </Button>
                    </div>}
                    <div className='button-wrapper'>
                        <Button
                            variant="contained"
                            color="secondary"
                            onClick={()=>{this.removeImage()}}
                            endIcon={<Delete />}
                        >
                            Удалить
                        </Button>
                    </div>
                </div>
                <div className='images-list'>
                    <ImagesList
                        images={dstImages}
                        title="dst"
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
