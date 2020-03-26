import React, { Component } from 'react';
import { PythonInterface } from 'reactopya';
import { Box, Button } from '@material-ui/core';
const config = require('./MainWidget.json');

export default class MainWidget extends Component {
    static title = 'Main widget for labbox_ephys'
    static reactopyaConfig = config
    constructor(props) {
        super(props);
        this.state = {
            // javascript state

            // python state
            status: '',
            status_message: ''
        }
    }
    componentDidMount() {
        this.pythonInterface = new PythonInterface(this, config);
        this.pythonInterface.start();
        this.setState({
            status: 'started',
            status_message: 'Starting python backend'
        });
        // Use this.pythonInterface.setState(...) to pass data to the python backend
        this.pythonInterface.setState({
            test: 1
        });
    }
    componentWillUnmount() {
        this.pythonInterface.stop();
    }
    render() {

        const style0 = {
            border: 'solid 3px gray',
            padding: 30,
            margin: 30
        };

        return (
            <div>
                <h3>Labbox Ephys</h3>
                <Box display="flex" flexDirection="row" p={1} m={1} style={{overflowX: 'hidden'}}>
                    <Box p={1} key="recordings" style={style0}>
                        <Button href={`recordingsview`}>View recordings</Button>
                    </Box>
                    <Box p={1} key="sortings" style={style0}>
                        <Button href={`sortingsview`}>View sortings</Button>
                    </Box>
                    <Box p={1} key="jupyter" style={style0}>
                        <Button href={`http://${location.hostname}:${this.props.jupyterlab_port}/lab`} target="_blank">Open jupyterlab</Button>
                    </Box>
                </Box>
            </div>
        )
    }
}
