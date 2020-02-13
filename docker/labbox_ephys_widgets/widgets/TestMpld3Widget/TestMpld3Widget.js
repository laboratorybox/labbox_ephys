import React, { Component } from 'react';
import { PythonInterface } from 'reactopya';
const config = require('./TestMpld3Widget.json');
const d3 = require('./d3.min.js');
console.log('d3=', d3);
window.mpld3 = require('./mpld3.v0.3.js');

export default class TestMpld3Widget extends Component {
    static title = 'testing mpld3 library'
    static reactopyaConfig = config
    constructor(props) {
        super(props);
        this.state = {
            // javascript state
            
            // python state
            status: '',
            status_message: '',
            plot: null
        }
        this.renderedPlots = {};
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
            test: 12
        });
    }
    componentDidUpdate() {
        const plot = this.state.plot;
        if (plot) {
            if (!this.renderedPlots[plot.id]) {
                mpld3.draw_figure(plot.id, plot.object);
                this.renderedPlots[plot.id] = true;
            }
        }
    }
    componentWillUnmount() {
        this.pythonInterface.stop();
    }
    render() {
        const plot = this.state.plot;
        if (plot) {
            return <div id={plot.id} />;
        }
        else {
            return <span>Loading.</span>;
        }
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