
import React, { Component } from 'react';
import { Table, TableHead, TableBody, TableRow, TableCell, Link, Checkbox } from '@material-ui/core';

export default class LBTable extends Component {
    state = {}
    _handleTableCellClick = (row, col) => {
        if (this.props.rowSelectionMode == 'single') {
            const { onSelectedRowIdsChanged } = this.props;
            let ids = {};
            ids[row.id] = true;
            onSelectedRowIdsChanged(ids);
        }
    }
    render() {
        const { columns, rows, rowSelectionMode, selectedRowIds, onSelectedRowIdsChanged } = this.props;
        let columns2 = [...columns];
        if (rowSelectionMode == 'multi') {
            columns2.splice(0, 0, {id:'_select_row', label: '', type: 'selectRow'})
        }
        function rowBackgroundColor(row) {
            if (row.id in (selectedRowIds || {}))
                return 'rgb(200, 200, 255)';
            else
                return '';
        }
        return (
            <Table>
                <TableHead>
                    <TableRow>
                        {
                            columns2.map((cc) => (
                                <TableCell key={cc.id}>{cc.label}</TableCell>
                            ))
                        }
                    </TableRow>
                </TableHead>
                <TableBody>
                    {
                        rows.map((row) => (
                            <TableRow key={row.id}>
                                {
                                    columns2.map((cc) => {
                                        let cell = row.cells[cc.id] || null;
                                        return (
                                            <TableCell key={cc.id} style={{backgroundColor: rowBackgroundColor(row)}} onClick={() => {this._handleTableCellClick(row, cc)}}>
                                                <CellContent
                                                    row={row}
                                                    column={cc}
                                                    cell={cell}
                                                    selectedRowIds={selectedRowIds || {}} 
                                                    onSelectedRowIdsChanged={onSelectedRowIdsChanged || function() {}}
                                                />
                                            </TableCell>
                                        );
                                    })
                                }
                            </TableRow>
                        ))
                    }
                </TableBody>
            </Table>
        );
    }
}

function CellContent(props) {
    const { cell, row, column, selectedRowIds, onSelectedRowIdsChanged } = props;
    if (column.type == 'selectRow') {
        return (
            <Checkbox
                checked={row.id in selectedRowIds}
                onChange={(evt, val) => {
                    if (val)
                        selectedRowIds[row.id] = true;
                    else
                        delete selectedRowIds[row.id];
                    onSelectedRowIdsChanged(selectedRowIds);
                }}
            />
        );
    }
    if (!cell) {
        return <span />;
    }
    if (cell.href) {
        return (
            <a href={cell.href} target={cell.target}>
                {cell.content}
            </a>
        )
    }
    else {
        return cell.content;
    }
}
