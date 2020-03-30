
import React, { Component } from 'react';
import LBTable from './LBTable';

export default class SortingsTable extends Component {
    render() {
        const { sortings, selectedSortingIds } = this.props;
        let columns = [
            {id: 'status', label: 'Status'},
            {id: 'sorter_name', label: 'Sorter'},
            {id: 'recording', label: 'Recording'},
            {id: 'group', label: 'Group/Shank'},
            {id: 'nunits', label: 'Num. units'}
        ];
        let rows = sortings.map((sorting) => {
            const href = `sortingview?sorting_id=${sorting.sorting_id}`;
            const target = '_blank'
            return {
                id: sorting.sorting_id,
                cells: {
                    status: {content: sorting.status || 'unknown', href: href, target: target},
                    recording: {content: sorting.recording_id},
                    group: {content: sorting.group_id},
                    sorter_name: {content: sorting.sorter_name},
                    nunits: {content: sorting.unit_ids ? sorting.unit_ids.length : ''}
                }
            }
        });
        return (
            <LBTable
                columns={columns}
                rows={rows}
                rowSelectionMode="multi"
                selectedRowIds={selectedSortingIds}
                onSelectedRowIdsChanged={(ids) => {this.props.onSelectedSortingIdsChanged(ids)}}
            />
        );
    }
}