import React, { Component } from 'react';
import { PythonInterface } from 'reactopya';
import SortingsTable from './SortingsTable.js'
const config = require('./SortingsView.json');

export default class SortingsView extends Component {
    static title = 'View database of sortings'
    static reactopyaConfig = config
    constructor(props) {
        super(props);
        this.state = {
            // javascript state
            
            // python state
            sortings: null,
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
        this.pythonInterface.setState({
            trigger: 1
        });
    }
    componentWillUnmount() {
        this.pythonInterface.stop();
    }
    _handleDeleteSortings = (sortingIds) => {
        this.pythonInterface.sendMessage({action: 'remove_sortings', sorting_ids: sortingIds});
    }
    render() {
        const sortings = this.state.sortings;

        if (!sortings) {
            return (
                <ReportStatus {...this.state} />
            );
        }

        return (
            <SortingsTable
                sortings={sortings}
                onDeleteSortings={this._handleDeleteSortings}
            />
        );
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