import React, { Component } from 'react';
import { PythonInterface } from 'reactopya';
import RecordingsTable from './RecordingsTable.js'
const config = require('./RecordingsView.json');

export default class RecordingsView extends Component {
    static title = 'View database of recordings'
    static reactopyaConfig = config
    constructor(props) {
        super(props);
        this.state = {
            // javascript state
            
            // python state
            recordings: null,
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
    _handleDeleteRecordings = (recordingIds) => {
        this.pythonInterface.sendMessage({name: 'deleteRecordings', recording_ids: recordingIds});
    }
    render() {
        const recordings = this.state.recordings;

        if (!recordings) {
            return (
                <ReportStatus {...this.state} />
            );
        }

        return (
            <RecordingsTable
                recordings={recordings}
                onDeleteRecordings={this._handleDeleteRecordings}
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