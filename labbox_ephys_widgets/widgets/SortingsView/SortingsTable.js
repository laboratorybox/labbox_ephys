
import React, { Component } from 'react';
import { Toolbar, IconButton } from '@material-ui/core';
import { FaTrash } from 'react-icons/fa';
import LBTable from './LBTable';

export default class SortingsTable extends Component {
    state = {
        selectedSortingIds: {}
    }
    _handleDeleteSelectedSortings = () => {
        this.props.onDeleteSortings && this.props.onDeleteSortings(Object.keys(this.state.selectedSortingIds));
    }
    render() {
        const { sortings } = this.props;
        const { selectedSortingIds } = this.state
        let columns = [
            {id: 'recording', label: 'Recording'},
            {id: 'group', label: 'Group/Shank'},
            {id: 'sorter_name', label: 'Sorter'},
            {id: 'nunits', label: 'Num. units'}
        ];
        let rows = sortings.map((rec) => {
            const href = `sortingview?sorting_id=${rec.sorting_id}`;
            const target = '_blank'
            return {
                id: rec.sorting_id,
                cells: {
                    recording: {content: rec.recording_id, href: href, target: target},
                    group: {content: rec.group_id, href: href, target: target},
                    sorter_name: {content: rec.sorter_name, href: href, target: target},
                    nunits: {content: rec.unit_ids.length, href: href, target: target}
                }
            }
        });
        return (
            <div>
                <Toolbar>
                    <IconButton disabled={isEmpty(selectedSortingIds)} title={"Delete selected sortings"} onClick={() => {this._handleDeleteSelectedSortings()}}>
                        <FaTrash />
                    </IconButton>
                </Toolbar>
                <LBTable
                    columns={columns}
                    rows={rows}
                    rowSelectionMode="multi"
                    selectedRowIds={selectedSortingIds}
                    onSelectedRowIdsChanged={(ids) => {this.setState({selectedSortingIds: ids})}}
                />
            </div>
        );
    }
}

function isEmpty(obj) {
    return (Object.getOwnPropertyNames(obj).length == 0);
}