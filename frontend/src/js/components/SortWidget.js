/**
 * Created by alexmelagrano on 5/9/18.
 */
import React from 'react';

export default class SortWidget extends React.Component {
    changeSort(e) {
        const targetValue = e.target.value.split(',');
        const sortEventType = targetValue[0];
        const sortTime = targetValue[1];

        this.props.context.updateSort(sortEventType, sortTime);
    }

    render() {
        return (
            <div className="d-flex align-items-center">
                <p className="mr-2 mb-0">Sort By:</p>
                <select onChange={this.changeSort.bind(this)} >
                    <option value={ [1, '*'] }>Total Drinks All Time</option>
                    <option value={ [1, '7d'] }>Total Drinks This Week</option>
                    <option value={ [1, '24h'] }>Total Drinks Today</option>
                </select>
            </div>
        )
    }
}
