
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
            {id: 'sorting', label: 'Sorting'},
            {id: 'nunits', label: 'Num. units'}
        ];
        let rows = sortings.map((rec) => (
            {
                id: rec.sorting_id,
                cells: {
                    sorting: {content: rec.sorting_id, href: `sortingview?sorting_id=${rec.sorting_id}`, target: '_blank'},
                    nunits: {content: rec.unit_ids.length}
                }
            }
        ));
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