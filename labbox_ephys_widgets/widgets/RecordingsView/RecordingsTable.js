
import React, { Component } from 'react';
import LBTable from './LBTable';

export default class RecordingsTable extends Component {
    render() {
        const { recordings } = this.props;
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
            <LBTable
                columns={columns}
                rows={rows}
                rowSelectionMode="multi"
                selectedRowIds={this.props.selectedRecordingIds}
                onSelectedRowIdsChanged={(ids) => {this.props.onSelectedRecordingIdsChanged(ids)}}
            />
        );
    }
}

