import React, { Component } from 'react';
import { PythonInterface } from 'reactopya';
import SortingsTable from './SortingsTable.js'
import { Toolbar, IconButton } from '@material-ui/core';
import { FaTrash, FaSync } from 'react-icons/fa';
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
            status_message: '',

            //
            selectedSortingIds: {}
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
    _handleDeleteSelectedSortings = () => {
        const selectedSortingIds = this.state.selectedSortingIds;
        this.pythonInterface.sendMessage({action: 'remove_sortings', sorting_ids: Object.keys(selectedSortingIds)});
    }
    _handleRefreshSortings = () => {
        this.setState({
            sortings: null,
            status: '',
            status_message: ''
        });
        this.pythonInterface.sendMessage({action: 'refresh_sortings'});
    }
    render() {
        const sortings = this.state.sortings;
        const selectedSortingIds = this.state.selectedSortingIds;

        let content;
        if (sortings) {
            content = (
                <SortingsTable
                    sortings={sortings}
                    selectedSortingIds={selectedSortingIds}
                    onSelectedSortingIdsChanged={(ids) => {this.setState({selectedSortingIds: ids})}}
                />
            )
        }
        else {
            content = (
                <ReportStatus {...this.state} />
            );
        }

        return (
            <div>
                <Toolbar>
                    <IconButton title={"Refresh sortings"} onClick={() => {this._handleRefreshSortings()}}>
                        <FaSync />
                    </IconButton>
                    <IconButton disabled={isEmpty(selectedSortingIds)} title={"Delete selected sortings"} onClick={() => {this._handleDeleteSelectedSortings()}}>
                        <FaTrash />
                    </IconButton>
                </Toolbar>
                <div style={{height: 250, overflowY: 'auto'}}>
                    {content}
                </div>
            </div>
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

function isEmpty(obj) {
    return (Object.getOwnPropertyNames(obj).length == 0);
}