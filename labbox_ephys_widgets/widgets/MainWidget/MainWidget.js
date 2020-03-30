import React, { Component } from 'react';
import { PythonInterface } from 'reactopya';
import { Box, Button, ThemeProvider, createMuiTheme } from '@material-ui/core';
import RecordingsView from '../RecordingsView/RecordingsView.js';
import SortingsView from '../SortingsView/SortingsView.js';
const config = require('./MainWidget.json');

const theme = createMuiTheme({
    typography: {
      // In Chinese and Japanese the characters are usually larger,
      // so a smaller fontsize may be appropriate.
      fontSize: 10,
    },
});

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
            padding: 0,
            margin: 10
        };

        return (
            <ThemeProvider theme={theme}>
            <div style={{margin: 20}}>
                <h2>Labbox Ephys</h2>
                <div>
                    <Box display="flex" flexDirection="row" p={1} m={1} style={{overflowX: 'hidden'}}>
                        <Box p={1} key="jupyter" style={style0}>
                            <Button href={`http://${location.hostname}:${this.props.jupyterlab_port}/lab`} target="_blank">Launch JupyterLab</Button>
                        </Box>
                    </Box>
                </div>
                <h3>Recordings</h3>
                    <RecordingsView
                        reactopyaParent={this}
                        reactopyaChildId={`RecordingsView`}
                    />
                <h3>Sortings</h3>
                    <SortingsView
                        reactopyaParent={this}
                        reactopyaChildId={`SortingsView`}
                    />
            </div>
            </ThemeProvider>
        )
    }
}

class OldMainWidget extends Component {
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
