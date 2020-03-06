import React, { Component } from 'react';
import { PythonInterface } from 'reactopya';
import { Table, TableHead, TableBody, TableRow, TableCell, Link, Checkbox, Box, Button } from '@material-ui/core';
import ElectrodeGeometryWidget from './ElectrodeGeometryWidget';
import './RecordingView.css';
const config = require('./RecordingView.json');

export default class RecordingView extends Component {
    static title = 'View a recording'
    static reactopyaConfig = config
    constructor(props) {
        super(props);
        this.state = {
            // javascript state
            recordingId: '',

            // python state
            recording: null,
            channel_ids: null,
            channel_groups: null,
            channel_locations: null,
            status: '',
            status_message: '',

            //
            selectedGroupId: null
        }
    }
    componentDidMount() {
        this.pythonInterface = new PythonInterface(this, config);
        this.pythonInterface.start();

        this.pythonInterface.setState({
            recording_id: this.props.recordingId || null,
            recording: this.props.recording || null,
            status: 'started',
            status_message: 'Starting'
        })
    }
    componentWillUnmount() {
        this.pythonInterface.stop();
    }
    render() {
        const { recording, channel_ids, channel_groups, channel_locations, selectedGroupId } = this.state;

        if (!recording) {
            return (
                <ReportStatus {...this.state} />
            );
        }

        let group_ids = get_all_group_ids(channel_groups || []);

        console.log('recording:', recording);
        return (
            <div>
                <RecordingViewTable
                    recording={recording}
                    channel_ids={channel_ids}
                    channel_groups={channel_groups}
                />
                <Box display="flex" flexDirection="row" p={1} m={1} style={{overflowX: 'auto'}}>
                    {
                        group_ids.map((id) => (
                            <Box p={1} key={id}>
                                <ShankBox
                                    group_id={id}
                                    channel_ids={filter_group(channel_ids, channel_groups, id)}
                                    channel_locations={filter_group(channel_locations, channel_groups, id)}
                                    selected={(id == selectedGroupId)}
                                    onClick={() => {this.setState({selectedGroupId: id})}}
                                />
                            </Box>
                        ))
                    }
                </Box>
                {
                    (selectedGroupId !== null) ? (
                        <a href={`timeseriesview?recording_id=${recording.recording_id}&group=${selectedGroupId}`}>
                            View timeseries for shank {selectedGroupId}
                        </a>                        
                    ) : <span />
                }
            </div>
        )
    }
}

class ShankBox extends Component {
    state = {}
    render() {
        const { group_id, channel_ids, channel_locations } = this.props;
        return (
            <div className={this.props.selected ? "ShankBox selected" : "ShankBox"} onClick={this.props.onClick}>
                <h3 style={{textAlign: "center"}}>Shank {group_id}</h3>
                <ElectrodeGeometryWidget
                    ids={channel_ids}
                    locations={channel_locations}
                />
            </div>
        );
    }
}

function filter_group(x, channel_groups, group_id) {
    let y = [];
    for (let ii=0; ii<x.length; ii++) {
        if (channel_groups[ii] == group_id) {
            y.push(x[ii]);
        }
    }
    return y;
}

function get_all_group_ids(channel_groups) {
    let x = {}
    for (let a of channel_groups) x[a] = true;
    let y = Object.keys(x);
    let z = [];
    for (let a of y) z.push(Number(a));
    z.sort();
    return z;
}

class RecordingViewTable extends Component {
    state = {
    }
    render() {
        const { recording, channel_ids, channel_groups } = this.props;
        return (
            <Table>
                <TableHead>
                </TableHead>
                <TableBody>
                    <TableRow>
                        <TableCell>Recording</TableCell>
                        <TableCell>{recording.recording_id}</TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell>Channel IDs</TableCell>
                        <TableCell>{commasep(channel_ids)}</TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell>Channel groups</TableCell>
                        <TableCell>{commasep(channel_groups)}</TableCell>
                    </TableRow>
                </TableBody>
            </Table>
        )
    }
}

function commasep(x) {
    if (!x) return JSON.stringify(x);
    return x.join(', ');
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