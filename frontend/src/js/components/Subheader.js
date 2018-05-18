/**
 * Created by alexmelagrano on 5/9/18.
 */
import React from 'react';

import SortWidget from './SortWidget';
import TimeLiveWidget from './TimeLiveWidget';

export default class Subheader extends React.Component {

    render() {
        return (
            <nav className="navbar navbar-expand-lg navbar-light bg-light">
                <div className="container">
                    <SortWidget context={ this.props.context } />
                    <TimeLiveWidget />
                </div>
            </nav>
        )
    }
}
