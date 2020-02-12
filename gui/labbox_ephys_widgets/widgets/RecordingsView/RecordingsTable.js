
import React, { Component } from 'react';
import { Toolbar, IconButton } from '@material-ui/core';
import { FaTrash } from 'react-icons/fa';
import LBTable from './LBTable';

export default class RecordingsTable extends Component {
    state = {
        selectedRecordingIds: {}
    }
    _handleDeleteSelectedRecordings = () => {
        this.props.onDeleteRecordings && this.props.onDeleteRecordings(Object.keys(this.state.selectedRecordingIds));
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
                    recording: {content: rec.recording_id, href: `timeseriesview?path=${rec.recording_path}`, target: '_blank'},
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

function isEmpty(obj) {
    return (Object.getOwnPropertyNames(obj).length == 0);
}