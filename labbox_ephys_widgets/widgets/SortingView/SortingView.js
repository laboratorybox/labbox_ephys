import React, { Component } from 'react';
import { PythonInterface } from 'reactopya';
import { Table, TableHead, TableBody, TableRow, TableCell, Link, Checkbox, Box } from '@material-ui/core';
import LBTable from './LBTable';
import SortingUnitView from '../SortingUnitView/SortingUnitView';
import SortingUnitsView from '../SortingUnitsView/SortingUnitsView';
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
            selectedUnitIds: {},

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
    _handleUnitClicked = (uid, evt) => {
        let suids = this.state.selectedUnitIds;
        if ((evt.ctrlKey) || (evt.shiftKey)) {
            if (uid in suids)
                delete suids[uid];
            else
                suids[uid] = true;
        }
        else {
            suids = {};
            suids[uid] = true;
        }
        this.setState({selectedUnitIds: suids});
    }
    render() {
        const { sorting, selectedUnitIds } = this.state;

        if (!sorting) {
            return (
                <ReportStatus {...this.state} />
            );
        }

        const unit_ids = sorting.unit_ids;

        let selectedUnitIdsList = Object.keys(selectedUnitIds).sort();

        let content = null;
        if (selectedUnitIdsList.length === 0) {
            content = <span />;
        }
        else if (selectedUnitIdsList.length === 1) {
            content = (
                <SortingUnitView
                    sorting={sorting}
                    unitId={selectedUnitIdsList[0]}
                    reactopyaParent={this}
                    reactopyaChildId={`SortingUnitView`}
                />
            );
        }
        else {
            content = (
                <SortingUnitsView
                    sorting={sorting}
                    unitIds={selectedUnitIdsList}
                    reactopyaParent={this}
                    reactopyaChildId={`SortingUnitsView`}
                />
            );
        }

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
                            <Box p={1} key={`box-${uid}`}>
                                <SortingUnitBox
                                    sorting={sorting}
                                    unitId={uid}
                                    reactopyaParent={this}
                                    reactopyaChildId={`SortingUnitView-${uid}`}
                                    onClick={(evt) => {this._handleUnitClicked(uid, evt)}}
                                    width={150}
                                    height={300}
                                    selected={(uid in selectedUnitIds)}
                                />
                            </Box>
                        ))
                    }
                </Box>
                {
                    content
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