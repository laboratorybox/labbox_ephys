import React, { Component } from 'react';
import { PythonInterface } from 'reactopya';
import RecordingsTable from './RecordingsTable.js'
import { Toolbar, IconButton } from '@material-ui/core';
import { FaTrash, FaSync } from 'react-icons/fa';
import Button from '@material-ui/core/Button';
import Menu from '@material-ui/core/Menu';
import MenuItem from '@material-ui/core/MenuItem';
const config = require('./RecordingsView.json');

const sorter_options = [
    {
        label: 'MountainSort4',
        sorter: {
            name: "mountainsort4",
            parameters: {}
        }
    },
    {
        label: 'KiloSort2',
        sorter: {
            name: "kilosort2",
            parameters: {}
        }
    }
];

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
            status_message: '',

            //
            selectedRecordingIds: {}
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
    _handleDeleteSelectedRecordings = () => {
        const recordingIds = this.state.selectedRecordingIds;
        this.pythonInterface.sendMessage({action: 'remove_recordings', recording_ids: recordingIds});
    }
    _handleSortSelectedRecordings = (sorter) => {
        const recordingIds = this.state.selectedRecordingIds;
        this.pythonInterface.sendMessage({action: 'sort_recordings', recording_ids: recordingIds, sorter: sorter});
    }
    _handleRefreshRecordings = () => {
        this.setState({
            recordings: null,
            status: '',
            status_message: ''
        });
        this.pythonInterface.sendMessage({action: 'refresh_recordings'});
    }
    render() {
        const recordings = this.state.recordings;
        const selectedRecordingIds = this.state.selectedRecordingIds;

        let content;
        if (recordings) {
            content = (
                <RecordingsTable
                    recordings={recordings}
                    selectedRecordingIds={this.state.selectedRecordingIds}
                    onSelectedRecordingIdsChanged={(ids) => {this.setState({selectedRecordingIds: ids})}}
                />
            );
        }
        else {
            content = (
                <ReportStatus {...this.state} />
            );
        }

        return (
            <div>
                <Toolbar>
                    <IconButton title={"Refresh recordings"} onClick={() => {this._handleRefreshRecordings()}}>
                        <FaSync />
                    </IconButton>
                    <IconButton disabled={isEmpty(selectedRecordingIds)} title={"Delete selected recordings"} onClick={() => {this._handleDeleteSelectedRecordings()}}>
                        <FaTrash />
                    </IconButton>
                    <DropdownMenu
                        label="Launch spike sorting"
                        disabled={isEmpty(selectedRecordingIds)} 
                        options={sorter_options}
                        onSorterSelected={(sorter) => {this._handleSortSelectedRecordings(sorter)}}
                    />
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

function DropdownMenu(props) {

    // return <div>Testing..... {JSON.stringify(props)}</div>;
    const [anchorEl, setAnchorEl] = React.useState(null);

    const handleClick = event => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };

    return (
        <div>
        <Button disabled={props.disabled} aria-controls="simple-menu" aria-haspopup="true" onClick={handleClick}>
            {props.label}
        </Button>
        <Menu
            id="simple-menu"
            anchorEl={anchorEl}
            keepMounted
            open={Boolean(anchorEl)}
            onClose={handleClose}
        >
            {
                props.options.map((option) => {
                    return (
                        <MenuItem
                            onClick={() => {handleClose(); props.onSorterSelected(option.sorter);}}
                            key={option.label}>{option.label}
                        </MenuItem>
                    );
                })
            }
        </Menu>
        </div>
    );
}

function isEmpty(obj) {
    return (Object.getOwnPropertyNames(obj).length == 0);
}