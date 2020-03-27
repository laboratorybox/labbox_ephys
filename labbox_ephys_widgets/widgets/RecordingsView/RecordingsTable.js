
import React, { Component } from 'react';
import { Toolbar, IconButton } from '@material-ui/core';
import { FaTrash } from 'react-icons/fa';
import Button from '@material-ui/core/Button';
import Menu from '@material-ui/core/Menu';
import MenuItem from '@material-ui/core/MenuItem';
import LBTable from './LBTable';

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

export default class RecordingsTable extends Component {
    state = {
        selectedRecordingIds: {}
    }
    _handleDeleteSelectedRecordings = () => {
        this.props.onDeleteRecordings && this.props.onDeleteRecordings(Object.keys(this.state.selectedRecordingIds));
    }
    _handleSortSelectedRecordings = (sorter) => {
        this.props.onSortRecordings && this.props.onSortRecordings(Object.keys(this.state.selectedRecordingIds), sorter);
    }
    render() {
        const { recordings } = this.props;
        const { selectedRecordingIds } = this.state
        let columns = [
            {id: 'recording', label: 'Recording'},
            {id: 'nchan', label: 'Num. channels'},
            {id: 'sampfreq', label: 'Samp. Freq. (Hz)'},
            {id: 'duration', label: 'Duration (sec)'}
        ];
        let rows = recordings.map((rec) => (
            {
                id: rec.recording_id,
                cells: {
                    recording: {content: rec.recording_id, href: `recordingview?recording_id=${rec.recording_id}`, target: '_blank'},
                    nchan: {content: rec.channel_ids.length},
                    sampfreq: {content: rec.sampling_frequency},
                    duration: {content: (rec.num_frames / rec.sampling_frequency)}
                }
            }
        ));
        return (
            <div>
                <Toolbar>
                    <IconButton disabled={isEmpty(selectedRecordingIds)} title={"Delete selected recordings"} onClick={() => {this._handleDeleteSelectedRecordings()}}>
                        <FaTrash />
                    </IconButton>
                    <DropdownMenu
                        label="Spike sorting"
                        options={sorter_options}
                        onSorterSelected={(sorter) => {this._handleSortSelectedRecordings(sorter)}}
                    />
                </Toolbar>
                <LBTable
                    columns={columns}
                    rows={rows}
                    rowSelectionMode="multi"
                    selectedRowIds={selectedRecordingIds}
                    onSelectedRowIdsChanged={(ids) => {this.setState({selectedRecordingIds: ids})}}
                />
            </div>
        );
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
        <Button aria-controls="simple-menu" aria-haspopup="true" onClick={handleClick}>
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
                    return <MenuItem onClick={() => {handleClose(); props.onSorterSelected(option.sorter);}} key={option.label}>{option.label}</MenuItem>
                })
            }
        </Menu>
        </div>
    );
}

function isEmpty(obj) {
    return (Object.getOwnPropertyNames(obj).length == 0);
}