import React, { Component } from 'react';
import { PythonInterface } from 'reactopya';
const config = require('./RecordingView2.json');

export default class RecordingView2 extends Component {
    static title = 'View a recording'
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
        return <div>
            This is a test Fan Wu.
        </div>
    }
}

