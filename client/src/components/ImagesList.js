import React from 'react'
import InputLabel from '@material-ui/core/InputLabel';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';

class ImagesList extends React.Component {
    render() {
        const { title, images } = this.props
        return (
            <FormControl className='form-control'>
                <InputLabel shrink>
                    {title}
                </InputLabel>
                <Select
                    multiple
                    native
                >
                    {Object.values(images).map(image => {
                        const key = image.name + ':' + image.tag
                        return (
                            <option key={key} value={key}>
                                {key}
                            </option>
                        )
                    })}
                </Select>
            </FormControl>
        )
    }
}

export default ImagesList