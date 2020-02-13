import React, { Component } from 'react';
import { PythonInterface } from 'reactopya';
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
        return (
            <div>
                <h3>Labbox Ephys</h3>
                <ul>
                    <li>
                        <a href={`recordingsview`}>
                            View recordings
                        </a>
                    </li>
                    <li>
                        <a href={`sortingsview`}>
                            View sortings
                        </a>
                    </li>
                    <li>
                        <a href={`http://${location.hostname}:${this.props.jupyterlab_port}/lab`} target="_blank">
                            Open JupyterLab
                        </a>
                    </li>
                    <li>
                        <a href={`directoryview?path=${this.props.local_data_dir||'/local-data'}`}>
                            View local ephys data
                        </a>
                    </li>
                    <li>
                        <a href={`timeseriesview?path=sha1dir://fb52d510d2543634e247e0d2d1d4390be9ed9e20.synth_magland/datasets_noise10_K10_C4/001_synth`}>
                            Example timeseries view
                        </a>
                    </li>
                </ul>
            </div>
            // <RespectStatus {...this.state}>
            //     <div>Render MainWidget here</div>
            // </RespectStatus>
        )
    }
}

class RespectStatus extends Component {
    state = {}
    render() {
        switch (this.props.status) {
            case 'started':
                return <div>Started: {this.props.status_message}</div>
            case 'running':
                return <div>{this.props.status_message}</div>
            case 'error':
                return <div>Error: {this.props.status_message}</div>
            case 'finished':
                return this.props.children;
            default:
                return <div>Unknown status: {this.props.status}</div>
        }
    }
}

