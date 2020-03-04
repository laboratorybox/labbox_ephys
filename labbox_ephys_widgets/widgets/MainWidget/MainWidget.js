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
                </ul>
            </div>
        )
    }
}
