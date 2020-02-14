import React, { Component } from 'react';
import { PythonInterface } from 'reactopya';
import SortingUnitTemplateWidget from '../SortingUnitTemplateWidget/SortingUnitTemplateWidget';
import "./SortingUnitBox.css";
const config = require('./SortingUnitBox.json');

export default class SortingUnitBox extends Component {
    static title = 'View a unit in a sorting result'
    static reactopyaConfig = config
    constructor(props) {
        super(props);
        this.state = {
            // javascript state
            sorting_id: '',
            
            // python state
            sorting: null,
            status: '',
            status_message: ''
        }
    }
    componentDidMount() {
        this.pythonInterface = new PythonInterface(this, config);
        this.pythonInterface.start();
        // Use this.pythonInterface.setState(...) to pass data to the python backend
        if (this.props.sortingId) {
            this.setState({
                status: 'started',
                status_message: 'Starting python backend'
            });
            this.pythonInterface.setState({
                sorting_id: this.props.sortingId
            });
        }
        else {
            this.setState({
                sorting: this.props.sorting
            })
        }
    }
    componentWillUnmount() {
        this.pythonInterface.stop();
    }
    render() {
        const { sorting } = this.state;
        const { unitId } = this.props;

        if (!sorting) {
            return (
                <ReportStatus {...this.state} />
            );
        }

        return (
            <div
                className={this.props.selected ? "SortingUnitView selected" : "SortingUnitView"}
                onClick={this.props.onClick || function() {}}
            >
                <h3 style={{textAlign: "center"}}>Unit {unitId}</h3>
                <SortingUnitTemplateWidget
                    sorting={sorting}
                    unitId={unitId}
                    reactopyaParent={this}
                    reactopyaChildId="SortingUnitTemplateWidget"
                    width={this.props.width}
                    height={this.props.height}
                />
            </div>
        )
    }
}

class ReportStatus extends Component {
    state = {}
    render() {
        switch (this.props.status) {
            case 'started':
                return <div>Started: {this.props.status_message}</div>;
            case 'running':
                return <div>{this.props.status_message}</div>;
            case 'error':
                return <div>Error: {this.props.status_message}</div>;
            case 'finished':
                return <div>Finished: {this.props.status_message}</div>;
            default:
                return <div>Unknown status: {this.props.status}</div>;
        }
    }
}