import React from 'react'
import InputLabel from '@material-ui/core/InputLabel'
import FormControl from '@material-ui/core/FormControl'
import Select from '@material-ui/core/Select'
import moment from 'moment'

const ALL_REPOS = '*'

class ImagesList extends React.Component {
    constructor(props) {
        super(props)
        this.state = {
            filteredImages: props.images,
            selectedRepo: ALL_REPOS
        }
        this.selectRepo = this.selectRepo.bind(this)
    }

    selectRepo(e) {
        const repo = e.target.value
        const {images} = this.props
        if (repo === ALL_REPOS) {
            this.setState({
                filteredImages: images,
                selectedRepo: ALL_REPOS
            })
            return
        }
        let filteredImages = {}
        filteredImages[repo] = images[repo]
        this.setState({
            filteredImages: filteredImages,
            selectedRepo: repo
        })
    }

    componentDidUpdate(prevProps) {
        if (prevProps.images === this.props.images) return

        let filteredImages = []
        let selectedRepo = ALL_REPOS
        if (this.state.selectedRepo !== ALL_REPOS
            && !!this.props.images[this.state.selectedRepo]) {
            filteredImages[this.state.selectedRepo] = this.props.images[this.state.selectedRepo]
            selectedRepo = this.state.selectedRepo
        } else {
            filteredImages = this.props.images
        }

        this.setState({
            filteredImages: filteredImages,
            selectedRepo: selectedRepo
        })
    }

    render() {
        const { title, images, selected, handleChange } = this.props
        const { filteredImages, selectedRepo } = this.state
        return (
            <FormControl className='form-control'>
                <InputLabel shrink>
                    {title}
                </InputLabel>
                <Select
                    value={selectedRepo}
                    onChange={this.selectRepo}
                    className="select-repo"
                >
                    <option key={ALL_REPOS} value={ALL_REPOS}>Все репозитории</option>
                    {Object.keys(images).map(repo => {
                        return (
                            <option key={repo} value={repo}>
                                {repo}
                            </option>
                        )
                    })}
                </Select>
                <Select
                    multiple
                    native
                    value={selected}
                    onChange={handleChange}
                >
                    {Object.keys(filteredImages).map(image => {
                        return filteredImages[image].map(tag => {
                            const key = image + ':' + tag.name
                            const created = tag.created * 1000
                            const date = moment(created).format("DD.MM.YYYY")
                            return (
                                <option key={key} value={key}>
                                    {key} ({ date })
                                </option>
                            )
                        })
                    })}
                </Select>
            </FormControl>
        )
    }
}

export default ImagesList