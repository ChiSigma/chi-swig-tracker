/**
 * Created by alexmelagrano on 5/9/18.
 */
import React from 'react';

import CardContainer from '../components/CardContainer';
import Navigation from '../components/Navigation';
import Subheader from '../components/Subheader';

export default class Layout extends React.Component {
    constructor() {
        super();

        this.eventTypes = [0, 1, 2]; // TODO :: make request to /api/event_types/
    }
    
    render() {
        return(
            <div>
                <Navigation />
                <Subheader />
                <CardContainer eventTypes={ this.eventTypes } />
                <p>[footer]</p>
            </div>
        )
    }
}