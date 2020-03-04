import React, { Component } from 'react';
import { PythonInterface } from 'reactopya';
import './mpld3_custom.css';
const config = require('./SortingUnitCorrelogramWidget.json');
const d3 = require('./d3.min.js');
console.log('d3=', d3);
window.mpld3 = require('./mpld3.v0.3.js');

export default class SortingUnitCorrelogramWidget extends Component {
    static title = 'Correlogram waveform of sorting unit'
    static reactopyaConfig = config
    constructor(props) {
        super(props);
        this.state = {
            // javascript state
            sorting: null,
            unit_id: null,
            
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
        this.update();
    }
    componentDidUpdate(prevProps, prevState) {
        if ((prevProps.sorting !== this.props.sorting) || (prevProps.unitId !== this.props.unitId)) {
            this.update();
        }
        const plot = this.state.plot;
        if (plot) {
            if (!this.renderedPlots[plot.id]) {
                let fig = mpld3.draw_figure(plot.id, plot.object);
                fig.toolbar.draw = function() {};
                window.fig=fig;
                this.renderedPlots[plot.id] = true;
            }
        }
    }
    update() {
        this.pythonInterface.setState({
            figsize: [this.props.width, this.props.height],
            sorting: this.props.sorting,
            unit_id: this.props.unitId
        });
        this.setState({plot: null});
    }
    componentWillUnmount() {
        this.pythonInterface.stop();
    }
    render() {
        const plot = this.state.plot;
        if (plot) {
            return (
                <div
                    id={plot.id}
                    key={plot.id}
                    // className={"hide-xaxis hide-yaxis"}
                    style={{width: this.props.width, height: this.props.height}}
                />
            );
        }
        else {
            return (
                <div
                    style={{width: this.props.width, height: this.props.height, background: 'rgb(230, 230, 235)'}}
                />
            );
        }
    }
}
