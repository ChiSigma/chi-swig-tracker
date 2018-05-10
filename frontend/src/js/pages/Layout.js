/**
 * Created by alexmelagrano on 5/9/18.
 */
import React from 'react';

import Navigation from '../components/Navigation';
import Subheader from '../components/Subheader';

export default class Layout extends React.Component {
    
    render() {
        return(
            <div>
                <Navigation />
                <Subheader />
                <p>[body]</p>
                <p>[footer]</p>
            </div>
        )
    }
}