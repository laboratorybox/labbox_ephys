import React, { Component } from 'react';
import { PythonInterface } from 'reactopya';
import { Table, TableHead, TableBody, TableRow, TableCell, Link, Checkbox, Box } from '@material-ui/core';
import LBTable from './LBTable';
import SortingUnitView from '../SortingUnitView/SortingUnitView';
import SortingUnitBox from '../SortingUnitBox/SortingUnitBox';
const config = require('./SortingView.json');

export default class SortingView extends Component {
    static title = 'View a sorting result'
    static reactopyaConfig = config
    constructor(props) {
        super(props);
        this.state = {
            // javascript state
            sortingId: '',
            selectedUnitId: null,

            // python state
            sorting: null,
            status: '',
            status_message: ''
        }
    }
    componentDidMount() {
        this.pythonInterface = new PythonInterface(this, config);
        this.pythonInterface.start();
        // Use this.pythonInterface.setState(...) to pass data to the python backend
        if (this.props.sortingId) {
            this.setState({
                status: 'started',
                status_message: 'Starting python backend'
            });
            this.pythonInterface.setState({
                sorting_id: this.props.sortingId
            });
        }
        else {
            this.setState({
                sorting: this.props.sorting
            })
        }
    }
    componentWillUnmount() {
        this.pythonInterface.stop();
    }
    _handleUnitClicked = (uid) => {
        this.setState({selectedUnitId: uid});
    }
    render() {
        const { sorting, selectedUnitId } = this.state;

        if (!sorting) {
            return (
                <ReportStatus {...this.state} />
            );
        }

        const unit_ids = sorting.unit_ids;

        return (
            <div>
                <SortingViewTable
                    sorting={sorting}
                />
                {/* <SortingUnitsTable
                    sorting={sorting}
                    selectedUnitIds={selectedUnitIds}
                    onSelectedUnitIdsChanged={(ids) => {this._handleSelectedUnitIdsChanged(ids)}}
                /> */}
                <Box display="flex" flexDirection="row" p={1} m={1} style={{overflowX: 'auto'}}>
                    {
                        unit_ids.map((uid) => (
                            <Box p={1}>
                                <SortingUnitBox
                                    sorting={sorting}
                                    unitId={uid}
                                    reactopyaParent={this}
                                    reactopyaChildId={`SortingUnitView-${uid}`}
                                    onClick={() => {this._handleUnitClicked(uid)}}
                                    width={150}
                                    height={300}
                                    selected={(uid == selectedUnitId)}
                                />
                            </Box>
                        ))
                    }
                </Box>
                {
                    selectedUnitId !== null ? (
                        <SortingUnitView
                            sorting={sorting}
                            unitId={selectedUnitId}
                            reactopyaParent={this}
                            reactopyaChildId={`SortingUnitView`}
                        />
                    ) : <span />
                }
            </div>
        )
    }
}

class SortingViewTable extends Component {
    state = {
    }
    render() {
        const { sorting } = this.props;
        return (
            <Table>
                <TableHead>
                </TableHead>
                <TableBody>
                    <TableRow>
                        <TableCell>Recording</TableCell>
                        <TableCell>{sorting.recording_id}</TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell>Sorting</TableCell>
                        <TableCell>{sorting.sorting_name}</TableCell>
                    </TableRow>
                    <TableRow>
                        <TableCell>Num. units</TableCell>
                        <TableCell>{sorting.unit_ids.length}</TableCell>
                    </TableRow>
                </TableBody>
            </Table>
        )
    }
}

class SortingUnitsTable extends Component {
    state = {
    }
    render() {
        const { sorting, selectedUnitIds, onSelectedUnitIdsChanged } = this.props;
        const unit_ids = sorting.unit_ids;
        let columns = [{ label: 'Unit', id: 'unit' }];
        let rows = unit_ids.map((id) => (
            { id: id, cells: { unit: { content: id } } }
        ));
        return (
            <div style={{ width: 180, height: 250, overflow: 'auto' }}>
                <LBTable
                    columns={columns}
                    rows={rows}
                    rowSelectionMode="single"
                    selectedRowIds={selectedUnitIds}
                    onSelectedRowIdsChanged={(ids) => { onSelectedUnitIdsChanged(ids) }}
                />
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