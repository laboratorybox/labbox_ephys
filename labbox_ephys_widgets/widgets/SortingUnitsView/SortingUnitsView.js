import React, { Component } from 'react';
import { PythonInterface } from 'reactopya';
import SortingUnitTemplateWidget from '../SortingUnitTemplateWidget/SortingUnitTemplateWidget';
import SortingUnitCorrelogramWidget from '../SortingUnitCorrelogramWidget/SortingUnitCorrelogramWidget';
import "./SortingUnitsView.css";
import { Box, Table, TableBody, TableRow, TableCell } from '@material-ui/core';
const config = require('./SortingUnitsView.json');

export default class SortingUnitsView extends Component {
    static title = 'View a unit in a sorting result'
    static reactopyaConfig = config
    constructor(props) {
        super(props);
        this.state = {
            // javascript state
            sorting_id: '',
            
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
    render() {
        const { sorting } = this.state;
        const { unitIds } = this.props;

        if (!sorting) {
            return (
                <ReportStatus {...this.state} />
            );
        }

        if (unitIds.length === 0) {
            return <span />;
        }
        const numUnits = unitIds.length;
        const widthPerUnit = 1000 / numUnits;

        return (
            <div
                className={this.props.selected ? "SortingUnitsView selected" : "SortingUnitsView"}
                onClick={this.props.onClick || function() {}}
            >
                <h3 style={{textAlign: "center"}}>Units {unitIds.join(', ')}</h3>
                <Table>
                    <TableBody>
                        {
                            unitIds.map((uid1) => (
                                <TableRow key={`row-${uid1}`}>
                                    {
                                        unitIds.map((uid2) => (
                                            <TableCell key={`col=${uid2}`}>
                                                <SortingUnitCorrelogramWidget
                                                    sorting={sorting}
                                                    unitId1={uid1}
                                                    unitId2={uid2}
                                                    reactopyaParent={this}
                                                    reactopyaChildId={`SortingUnitCorrelogramWidget-${uid1}-${uid2}`}
                                                    width={widthPerUnit}
                                                    height={widthPerUnit}
                                                />
                                            </TableCell>
                                        ))
                                    }
                                </TableRow>
                            ))
                        }
                    </TableBody>
                </Table>
                {/* <Box display="flex" flexDirection="row" p={2} m={2}>
                    
                </Box> */}
            </div>
        )
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